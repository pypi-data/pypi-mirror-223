import asyncio
from dataclasses import is_dataclass
import inspect
import contextvars
from inspect import iscoroutine
from typing import Type, TypeVar, Dict
from .exceptions import ResolverTargetAttrNotFound, LoaderFieldNotProvidedError, MissingAnnotationError
from typing import Any, Callable, Optional
from pydantic_resolve import core
from aiodataloader import DataLoader
from inspect import isclass
from types import MappingProxyType
from pydantic import BaseModel
import pydantic_resolve.constant as const
import pydantic_resolve.util as util


def LoaderDepend(  # noqa: N802
    dependency: Optional[Callable[..., Any]] = None,
) -> Any:
    return Depends(dependency=dependency)

class Depends:
    def __init__(
        self, 
        dependency: Optional[Callable[..., Any]] = None,
    ):
        self.dependency = dependency

T = TypeVar("T")

class Resolver:
    """
    Entrypoint of a resolve action
    """
    def __init__(
            self, 
            loader_filters: Optional[Dict[Any, Dict[str, Any]]] = None, 
            loader_instances: Optional[Dict[Any, Any]] = None,
            annotation_class: Optional[Type] = None,
            ensure_type=False,
            context: Optional[Dict[str, Any]] = None
            ):
        self.ctx = {}

        # for dataloader which has class attributes, you can assign the value at here
        self.loader_filters = loader_filters or {}

        # now you can pass your loader instance, Resolver will check isinstance
        if loader_instances and self.validate_instance(loader_instances):
            self.loader_instances = loader_instances
        else:
            self.loader_instances = None

        self.ensure_type = ensure_type
        self.annotation_class = annotation_class
        self.context = context
    
    def validate_instance(self, loader_instances: Dict[Any, Any]):
        for cls, loader in loader_instances.items():
            if not issubclass(cls, DataLoader):
                raise AttributeError(f'{cls.__name__} must be subclass of DataLoader')
            if not isinstance(loader, cls):
                raise AttributeError(f'{loader.__name__} is not instance of {cls.__name__}')
        return True

    def exec_method(self, method):
        """
        1. inspect method
        2. if params has LoaderDepend, manage the creation of dataloader
            2.1 handle DataLoader class
                2.1.1 handle dataloader filter config
            2.2 handle batch_load_fn
        """

        # >>> 1
        signature = inspect.signature(method)
        params = {}

        if signature.parameters.get('context'):
            if self.context is None:
                raise AttributeError('Resolver.context is missing')
            params['context'] = MappingProxyType(self.context)

        # manage the creation of loader instances
        for k, v in signature.parameters.items():

            # >>> 2
            if isinstance(v.default, Depends):
                # Base: DataLoader or batch_load_fn
                Loader = v.default.dependency

                # check loader_instance first, if has predefined loader instance, just use it.
                if self.loader_instances and self.loader_instances.get(Loader):
                    loader = self.loader_instances.get(Loader)
                    params[k] = loader
                    continue

                # module.kls to avoid same kls name from different module
                cache_key = f'{v.default.dependency.__module__}.{v.default.dependency.__name__}'
                hit = self.ctx.get(cache_key)
                if hit:
                    loader = hit
                else:
                    # >>> 2.1
                    # create loader instance 
                    if isclass(Loader):
                        # if extra transform provides
                        loader = Loader()

                        filter_config = self.loader_filters.get(Loader, {})

                        for field in util.get_class_field_annotations(Loader):
                        # >>> 2.1.1
                        # class ExampleLoader(DataLoader):
                        #     filtar_x: bool  <--------------- set this field
                            try:
                                value = filter_config[field]
                                setattr(loader, field, value)
                            except KeyError:
                                raise LoaderFieldNotProvidedError(f'{cache_key}.{field} not found in Resolver()')

                    # >>> 2.2
                    # build loader from batch_load_fn, filters config is impossible
                    else:
                        loader = DataLoader(batch_load_fn=Loader) # type:ignore

                    self.ctx[cache_key] = loader
                params[k] = loader
        return method(**params)


    async def _resolve_obj_field(self, target, field, attr):
        """
        resolve object fields
        1. validations
        2. exec methods
        3. parse to target type & resolve
        4. set back value
        """

        # >>> 1
        target_attr_name = str(field).replace(const.PREFIX, '')

        if not hasattr(target, target_attr_name):
            raise ResolverTargetAttrNotFound(f"attribute {target_attr_name} not found")

        if self.ensure_type:
            if not attr.__annotations__:
                raise MissingAnnotationError(f'{field}: return annotation is required')

        # >>> 2
        val = self.exec_method(attr)
        while iscoroutine(val) or asyncio.isfuture(val):
            val = await val

        # >>> 3
        if not getattr(attr, const.HAS_MAPPER_FUNCTION, False):  # defined in util.mapper
            val = util.try_parse_data_to_target_field_type(target, target_attr_name, val)

        val = await self._resolve(val)

        # >>> 4
        setattr(target, target_attr_name, val)


    async def _resolve(self, target: T) -> T:
        """ 
        resolve dataclass object or pydantic object / or list in place 

        1. iterate over elements if target is list
        2. resolve object
            2.1 resolve each single resolver fn and object fields
            2.2 execute post fn
        """

        # >>> 1
        if isinstance(target, (list, tuple)):
            await asyncio.gather(*[self._resolve(t) for t in target])

        # >>> 2
        if core.is_acceptable_type(target):
            tasks = []
            # >>> 2.1
            for field, attr, _type in core.iter_over_object_resolvers_and_acceptable_fields(target):
                if _type == const.ATTRIBUTE: tasks.append(self._resolve(attr))
                if _type == const.RESOLVER: tasks.append(self._resolve_obj_field(target, field, attr))

            await asyncio.gather(*tasks)

            # >>> 2.2
            # execute post methods, take no params
            for post_key in core.iter_over_object_post_methods(target):
                post_attr_name = post_key.replace(const.POST_PREFIX, '')
                if not hasattr(target, post_attr_name):
                    raise ResolverTargetAttrNotFound(f"fail to run {post_key}(), attribute {post_attr_name} not found")

                post_method = target.__getattribute__(post_key)
                calc_result = post_method()
                setattr(target, post_attr_name, calc_result)
            
            # hidden entry for performance. run at last
            default_post_method = getattr(target, const.POST_DEFAULT_HANDLER, None)
            if default_post_method:
                default_post_method()

        return target

    async def resolve(self, target: T) -> T:
        # if raise forwardref related error, use this
        if self.annotation_class:
            if issubclass(self.annotation_class, BaseModel):
                util.update_forward_refs(self.annotation_class)

            if is_dataclass(self.annotation_class):
                util.update_dataclass_forward_refs(self.annotation_class)

        await self._resolve(target)
        return target 