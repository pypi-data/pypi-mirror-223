"""Base classes for all algorithms.

Each module in this package defines a single algorithm.

Attributes:
    registry: A read-only dictionary of algorithm factory names to their
              implementation classes.
"""
from __future__ import annotations

from abc import ABC
import inspect
from types import MappingProxyType
from typing import Any, Callable, ClassVar, Dict, Mapping, Optional, Type, TypeVar

from decorator import decorate
from typing_extensions import ParamSpec

from bitfount.federated.exceptions import AlgorithmError
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.federated.roles import _RolesMixIn
from bitfount.federated.types import AlgorithmType
from bitfount.types import T_FIELDS_DICT, T_NESTED_FIELDS, _BaseSerializableObjectMixIn

logger = _get_federated_logger(__name__)

_P = ParamSpec("_P")
_R = TypeVar("_R")


class _BaseAlgorithm(ABC):
    """Blueprint for either the modeller side or the worker side of BaseAlgorithm."""

    def __init__(self, **kwargs: Any):
        super().__init__()

    @classmethod
    def exception_handler(cls, func: Callable[_P, _R]) -> Callable[_P, Optional[_R]]:
        """Log exceptions raised to federated logger.

        Also re-raise the exception to the caller with more context.
        """

        def federated_exception(
            cls: _BaseAlgorithm, *args: _P.args, **kwargs: _P.kwargs
        ) -> Optional[_R]:
            try:
                r = func(*args, **kwargs)
                return r
            except Exception as e:
                # TODO: [BIT-1619] change to federated_exception
                logger.federated_error(str(e))
                raise AlgorithmError(
                    f"Algorithm function {func.__name__} from {cls.__module__} "
                    f"raised the following exception: {e}"
                ) from e

        return decorate(func, federated_exception)


class BaseModellerAlgorithm(_BaseAlgorithm, ABC):
    """Modeller side of the algorithm."""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)


class BaseWorkerAlgorithm(_BaseAlgorithm, ABC):
    """Worker side of the algorithm."""

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def __init_subclass__(cls, **kwargs: Any):
        if not (inspect.isabstract(cls) or ABC in cls.__bases__):
            if hasattr(cls, "run"):
                # Decorate the `run` method to log exceptions and fail gracefully.
                cls.run = cls.exception_handler(cls.run)
            else:
                raise AttributeError(
                    f"Worker algorithm {cls.__name__} does not have a `run` method;"
                    f" all subclasses should implement a `run()`."
                )
            if hasattr(cls, "initialise"):
                # Decorate the `initialise` method to log
                # exceptions and fail gracefully.
                cls.initialise = cls.exception_handler(cls.initialise)
            else:
                raise AttributeError(
                    f"Worker algorithm {cls.__name__} does not have a `initialise`"
                    f" method; all subclasses should implement a `initialise()`."
                )

    def _apply_pod_dp(self, pod_dp: Optional[DPPodConfig]) -> None:
        """Applies pod-level Differential Privacy constraints.

        Subclasses should override this method if DP is supported.

        Args:
            pod_dp: The pod DP constraints to apply or None if no constraints.
        """
        pass


# The mutable underlying dict that holds the registry information
_registry: Dict[str, Type[BaseAlgorithmFactory]] = {}
# The read-only version of the registry that is allowed to be imported
registry: Mapping[str, Type[BaseAlgorithmFactory]] = MappingProxyType(_registry)


class BaseAlgorithmFactory(ABC, _RolesMixIn, _BaseSerializableObjectMixIn):
    """Base algorithm factory from which all other algorithms must inherit.

    Attributes:
       class_name: The name of the algorithm class.
    """

    fields_dict: ClassVar[T_FIELDS_DICT] = {}
    nested_fields: ClassVar[T_NESTED_FIELDS] = {}

    def __init__(self, **kwargs: Any):
        try:
            self.class_name = AlgorithmType[type(self).__name__].value
        except KeyError:
            # Check if the algorithm is a plug-in
            self.class_name = type(self).__name__
        super().__init__(**kwargs)

    @classmethod
    def __init_subclass__(cls, **kwargs: Any):
        if not inspect.isabstract(cls):
            logger.debug(f"Adding {cls.__name__}: {cls} to Algorithm registry")
            _registry[cls.__name__] = cls
