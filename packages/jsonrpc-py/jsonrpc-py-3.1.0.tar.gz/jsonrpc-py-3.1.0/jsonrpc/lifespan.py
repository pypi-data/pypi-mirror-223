from collections.abc import Callable, Generator, MutableSet
from dataclasses import dataclass, field
from typing import Any, Final, TypeAlias, TypeVar
from weakref import WeakSet

from .typedefs import ASGIReceiveCallable, ASGISendCallable
from .utilities import CancellableGather, ensure_async

__all__: Final[tuple[str, ...]] = (
    "LifespanEvents",
    "LifespanManager",
)

AnyCallable: TypeAlias = Callable[..., Any]
Func = TypeVar("Func", bound=AnyCallable)


@dataclass(slots=True, weakref_slot=True)
class LifespanEvents:
    """
    Simple class for storing the user-defined functions that running
    when application is initiated and shutting down.
    """

    #: The :py:class:`collections.abc.MutableSet` collection of startup functions.
    startup_events: MutableSet[AnyCallable] = field(default_factory=WeakSet)

    #: The :py:class:`collections.abc.MutableSet` collection of shutdown functions.
    shutdown_events: MutableSet[AnyCallable] = field(default_factory=WeakSet)

    def on_startup(self, user_function: Func, /) -> Func:
        """
        Decorator for the adding a function which will be executed
        when application is initiated.

        Example usage::

            >>> @app.events.on_startup
            ... def startup_callback() -> None:
            ...     print("Some important message.")

        :param user_function: The :py:class:`collections.abc.Callable` object representing the user-defined function.
        :returns: The unmodified ``user_function`` object, passed in the parameters.
        """
        self.startup_events.add(user_function)
        return user_function

    def on_shutdown(self, user_function: Func, /) -> Func:
        """
        Decorator for the adding a function which will be executed
        when application is shutting down.

        Example usage::

            >>> @app.events.on_shutdown
            ... async def shutdown_callback() -> None:
            ...     await important_function()

        :param user_function: The :py:class:`collections.abc.Callable` object representing the user-defined function.
        :returns: The unmodified ``user_function`` object, passed in the parameters.
        """
        self.shutdown_events.add(user_function)
        return user_function


@dataclass(slots=True)
class LifespanManager:
    receive: ASGIReceiveCallable
    send: ASGISendCallable
    events: LifespanEvents

    def __await__(self) -> Generator[Any, None, None]:
        #: ---
        #: Create a suitable iterator by calling __await__ on a coroutine.
        return self.__await_impl__().__await__()

    async def __await_impl__(self) -> None:
        match await self.receive():
            case {"type": "lifespan.startup"}:
                try:
                    if startup_events := self.events.startup_events:
                        await CancellableGather(map(ensure_async, startup_events))
                except BaseException:
                    await self.send({"type": "lifespan.startup.failed"})
                    raise
                else:
                    await self.send({"type": "lifespan.startup.complete"})
            case {"type": "lifespan.shutdown"}:
                try:
                    if shutdown_events := self.events.shutdown_events:
                        await CancellableGather(map(ensure_async, shutdown_events))
                except BaseException:
                    await self.send({"type": "lifespan.shutdown.failed"})
                    raise
                else:
                    await self.send({"type": "lifespan.shutdown.complete"})
