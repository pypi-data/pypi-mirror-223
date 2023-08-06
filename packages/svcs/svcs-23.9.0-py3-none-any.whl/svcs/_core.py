# SPDX-FileCopyrightText: 2023 Hynek Schlawack <hs@ox.cx>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import inspect
import logging
import sys
import warnings

from collections.abc import Callable
from contextlib import suppress
from inspect import isasyncgenfunction, isawaitable, iscoroutinefunction
from typing import Any, AsyncGenerator, Generator, TypeVar, overload

import attrs

from .exceptions import ServiceNotFoundError


log = logging.getLogger(__name__)

if sys.version_info < (3, 10):

    def anext(gen: AsyncGenerator) -> Any:
        return gen.__anext__()


@attrs.frozen
class RegisteredService:
    svc_type: type
    factory: Callable = attrs.field(hash=False)
    takes_container: bool
    is_async: bool
    ping: Callable | None = attrs.field(hash=False)

    @property
    def name(self) -> str:
        return f"{ self.svc_type.__module__ }.{self.svc_type.__qualname__}"

    def __repr__(self) -> str:
        return (
            f"<RegisteredService(svc_type="
            f"{self.name}, "
            f"{self.factory}, "
            f"takes_container={self.takes_container}, "
            f"has_ping={ self.ping is not None}"
            ")>"
        )


@attrs.frozen
class ServicePing:
    _container: Container
    _rs: RegisteredService

    def ping(self) -> None:
        svc: Any = self._container.get(self._rs.svc_type)
        self._rs.ping(svc)  # type: ignore[misc]

    async def aping(self) -> None:
        svc: Any = await self._container.aget(self._rs.svc_type)
        if iscoroutinefunction(self._rs.ping):
            await self._rs.ping(svc)
        else:
            self._rs.ping(svc)  # type: ignore[misc]

    @property
    def name(self) -> str:
        return self._rs.name

    @property
    def is_async(self) -> bool:
        """
        Return True if you have to use `aping` instead of `ping`.
        """
        return self._rs.is_async or iscoroutinefunction(self._rs.ping)


@attrs.define
class Registry:
    _services: dict[type, RegisteredService] = attrs.Factory(dict)
    _on_close: list[tuple[str, Callable]] = attrs.Factory(list)

    def __repr__(self) -> str:
        return f"<svcs.Registry(num_services={len(self._services)})>"

    def __contains__(self, svc_type: type) -> bool:
        return svc_type in self._services

    def __enter__(self) -> Registry:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    async def __aenter__(self) -> Registry:
        return self

    async def __aexit__(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        await self.aclose()

    def register_factory(
        self,
        svc_type: type,
        factory: Callable,
        *,
        ping: Callable | None = None,
        on_registry_close: Callable | None = None,
    ) -> None:
        """
        Register *factory* for *svc_type*.

        Args:
            svc_type: The type of the service to register.

            factory: A callable that is used to instantiated *svc_type* if
                asked. If it's a generator, a cleanup is registered after
                instantiation. Can be also async or an async generator.

            ping: A callable that marks the service as having a health check.
                The service iss returned when :meth:`Container.get_pings` is
                called and *ping* is called as part of :meth:`ServicePing.ping`
                or :meth:`ServicePing.aping`.

            on_registry_close: A callable that is called when the
                :meth:`Registry.close()` method is called. Can be async, then
                :meth:`Registry.aclose()` must be called.
        """
        rs = RegisteredService(
            svc_type,
            factory,
            _takes_container(factory),
            iscoroutinefunction(factory) or isasyncgenfunction(factory),
            ping,
        )
        self._services[svc_type] = rs

        if on_registry_close is not None:
            self._on_close.append((rs.name, on_registry_close))

    def register_value(
        self,
        svc_type: type,
        value: object,
        *,
        ping: Callable | None = None,
        on_registry_close: Callable | None = None,
    ) -> None:
        """
        Syntactic sugar for ``register_factory(svc_type, lambda: value,
        ping=ping, on_registry_close=on_registry_close)``.
        """
        self.register_factory(
            svc_type,
            lambda: value,
            ping=ping,
            on_registry_close=on_registry_close,
        )

    def get_registered_service_for(self, svc_type: type) -> RegisteredService:
        try:
            return self._services[svc_type]
        except KeyError:
            raise ServiceNotFoundError(svc_type) from None

    def close(self) -> None:
        """
        Clear registrations & run synchronous ``on_registry_close`` callbacks.
        """
        for name, oc in reversed(self._on_close):
            if iscoroutinefunction(oc):
                warnings.warn(
                    f"Skipped async cleanup for {name!r}. "
                    "Use aclose() instead.",
                    # stacklevel doesn't matter here; it's coming from a
                    # framework.
                    stacklevel=1,
                )
                continue

            try:
                log.debug("closing %r", name)
                oc()
                log.debug("closed %r", name)
            except Exception:  # noqa: BLE001
                log.warning(
                    "Registry's on_registry_close hook failed for %r.",
                    name,
                    exc_info=True,
                    extra={"svcs_service_name": name},
                )

        self._services.clear()
        self._on_close.clear()

    async def aclose(self) -> None:
        """
        Clear registrations & run all ``on_registry_close`` callbacks.
        """
        for name, oc in reversed(self._on_close):
            try:
                if iscoroutinefunction(oc) or isawaitable(oc):
                    log.debug("async closing %r", name)
                    await oc()
                    log.debug("async closed %r", name)
                else:
                    log.debug("closing %r", name)
                    oc()
                    log.debug("closed %r", name)
            except Exception:  # noqa: BLE001, PERF203
                log.warning(
                    "Registry's on_registry_close hook failed for %r.",
                    name,
                    exc_info=True,
                    extra={"svcs_service_name": name},
                )

        self._services.clear()
        self._on_close.clear()


def _takes_container(factory: Callable) -> bool:
    """
    Return True if *factory* takes a svcs.Container as its first argument.
    """
    sig = inspect.signature(factory)
    if not sig.parameters:
        return False

    if len(sig.parameters) != 1:
        msg = "Factories must take 0 or 1 parameters."
        raise TypeError(msg)

    ((name, p),) = tuple(sig.parameters.items())
    if name == "svcs_container":
        return True

    if (annot := p.annotation) is Container or annot == "svcs.Container":
        return True

    return False


T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
T5 = TypeVar("T5")
T6 = TypeVar("T6")
T7 = TypeVar("T7")
T8 = TypeVar("T8")
T9 = TypeVar("T9")
T10 = TypeVar("T10")


@attrs.define
class Container:
    """
    A per-context container for instantiated services & cleanups.
    """

    registry: Registry
    _instantiated: dict[type, object] = attrs.Factory(dict)
    _on_close: list[tuple[str, Generator | AsyncGenerator]] = attrs.Factory(
        list
    )

    def __repr__(self) -> str:
        return (
            f"<Container(instantiated={len(self._instantiated)}, "
            f"cleanups={len(self._on_close)})>"
        )

    def __contains__(self, svc_type: type) -> bool:
        return svc_type in self._instantiated

    def __enter__(self) -> Container:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    async def __aenter__(self) -> Container:
        return self

    async def __aexit__(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        await self.aclose()

    def forget_about(self, svc_type: type) -> None:
        """
        Remove all traces of *svc_type* from ourselves.
        """
        with suppress(KeyError):
            del self._instantiated[svc_type]

    def close(self) -> None:
        """
        Run all registered *synchronous* cleanups.

        Async closes are *not* awaited.
        """
        for name, gen in reversed(self._on_close):
            try:
                if isinstance(gen, AsyncGenerator):
                    warnings.warn(
                        f"Skipped async cleanup for {name!r}. "
                        "Use aclose() instead.",
                        # stacklevel doesn't matter here; it's coming from a framework.
                        stacklevel=1,
                    )
                    continue

                next(gen)

                warnings.warn(
                    f"Container clean up for {name!r} didn't stop iterating.",
                    stacklevel=1,
                )
            except StopIteration:  # noqa: PERF203
                pass
            except Exception:  # noqa: BLE001
                log.warning(
                    "Container clean up failed for %r.",
                    name,
                    exc_info=True,
                    extra={"svcs_service_name": name},
                )

        self._on_close.clear()
        self._instantiated.clear()

    async def aclose(self) -> None:
        """
        Run *all* registered cleanups -- synchronous **and** asynchronous.
        """
        for name, gen in reversed(self._on_close):
            try:
                if isinstance(gen, AsyncGenerator):
                    await anext(gen)
                else:
                    next(gen)

                warnings.warn(
                    f"Container clean up for {name!r} didn't stop iterating.",
                    stacklevel=1,
                )

            except (StopAsyncIteration, StopIteration):  # noqa: PERF203
                pass
            except Exception:  # noqa: BLE001
                log.warning(
                    "Container clean up failed for %r.",
                    name,
                    exc_info=True,
                    extra={"svcs_service_name": name},
                )

        self._on_close.clear()
        self._instantiated.clear()

    def get_pings(self) -> list[ServicePing]:
        """
        Get all pingable services and bind them to ourselves for cleanups.
        """
        return [
            ServicePing(self, rs)
            for rs in self.registry._services.values()
            if rs.ping is not None
        ]

    def get_abstract(self, *svc_types: type) -> Any:
        """
        Like :meth:`get` but is annotated to return `Any` which allows it to be
        used with abstract types like :class:`typing.Protocol` or :mod:`abc`
        classes.

        Note:
             See https://github.com/python/mypy/issues/4717 why this is
             necessary.
        """
        return self.get(*svc_types)

    async def aget_abstract(self, *svc_types: type) -> Any:
        """
        Like :meth:`aget` but has returns `Any` which allows it to be used with
        abstract types like :class:`typing.Protocol` or :mod:`abc` classes.
        """
        return await self.aget(*svc_types)

    @overload
    def get(self, svc_type: type[T1], /) -> T1:
        ...

    @overload
    def get(
        self, svc_type1: type[T1], svc_type2: type[T2], /
    ) -> tuple[T1, T2]:
        ...

    @overload
    def get(
        self, svc_type1: type[T1], svc_type2: type[T2], svc_type3: type[T3], /
    ) -> tuple[T1, T2, T3]:
        ...

    @overload
    def get(
        self,
        svc_type1: type[T1],
        svc_type2: type[T2],
        svc_type3: type[T3],
        svc_type4: type[T4],
        /,
    ) -> tuple[T1, T2, T3, T4]:
        ...

    @overload
    def get(
        self,
        svc_type1: type[T1],
        svc_type2: type[T2],
        svc_type3: type[T3],
        svc_type4: type[T4],
        svc_type5: type[T5],
        /,
    ) -> tuple[T1, T2, T3, T4, T5]:
        ...

    @overload
    def get(
        self,
        svc_type1: type[T1],
        svc_type2: type[T2],
        svc_type3: type[T3],
        svc_type4: type[T4],
        svc_type5: type[T5],
        svc_type6: type[T6],
        /,
    ) -> tuple[T1, T2, T3, T4, T5, T6]:
        ...

    @overload
    def get(
        self,
        svc_type1: type[T1],
        svc_type2: type[T2],
        svc_type3: type[T3],
        svc_type4: type[T4],
        svc_type5: type[T5],
        svc_type6: type[T6],
        svc_type7: type[T7],
        /,
    ) -> tuple[T1, T2, T3, T4, T5, T6, T7]:
        ...

    @overload
    def get(
        self,
        svc_type1: type[T1],
        svc_type2: type[T2],
        svc_type3: type[T3],
        svc_type4: type[T4],
        svc_type5: type[T5],
        svc_type6: type[T6],
        svc_type7: type[T7],
        svc_type8: type[T8],
        /,
    ) -> tuple[T1, T2, T3, T4, T5, T6, T7, T8]:
        ...

    @overload
    def get(
        self,
        svc_type1: type[T1],
        svc_type2: type[T2],
        svc_type3: type[T3],
        svc_type4: type[T4],
        svc_type5: type[T5],
        svc_type6: type[T6],
        svc_type7: type[T7],
        svc_type8: type[T8],
        svc_type9: type[T9],
        /,
    ) -> tuple[T1, T2, T3, T4, T5, T6, T7, T8, T9]:
        ...

    @overload
    def get(
        self,
        svc_type1: type[T1],
        svc_type2: type[T2],
        svc_type3: type[T3],
        svc_type4: type[T4],
        svc_type5: type[T5],
        svc_type6: type[T6],
        svc_type7: type[T7],
        svc_type8: type[T8],
        svc_type9: type[T9],
        svc_type10: type[T10],
        /,
    ) -> tuple[T1, T2, T3, T4, T5, T6, T7, T8, T9, T10]:
        ...

    def get(self, *svc_types: type) -> object:
        """
        Get an instance of *svc_type*s.

        Instantiate them if necessary and register their cleanup.

        Returns:
             If one service is requested, it's returned directly. If multiple
             are requested, a sequence of services is returned.
        """
        rv = []
        for svc_type in svc_types:
            if (svc := self._instantiated.get(svc_type)) is not None:
                rv.append(svc)
                continue

            rs = self.registry.get_registered_service_for(svc_type)
            svc = rs.factory(self) if rs.takes_container else rs.factory()

            if isinstance(svc, Generator):
                self._on_close.append((rs.name, svc))
                svc = next(svc)

            self._instantiated[svc_type] = svc

            rv.append(svc)

        if len(rv) == 1:
            return rv[0]

        return rv

    @overload
    async def aget(self, svc_type: type[T1], /) -> T1:
        ...

    @overload
    async def aget(
        self, svc_type1: type[T1], svc_type2: type[T2], /
    ) -> tuple[T1, T2]:
        ...

    @overload
    async def aget(
        self, svc_type1: type[T1], svc_type2: type[T2], svc_type3: type[T3], /
    ) -> tuple[T1, T2, T3]:
        ...

    @overload
    async def aget(
        self,
        svc_type1: type[T1],
        svc_type2: type[T2],
        svc_type3: type[T3],
        svc_type4: type[T4],
        /,
    ) -> tuple[T1, T2, T3, T4]:
        ...

    @overload
    async def aget(
        self,
        svc_type1: type[T1],
        svc_type2: type[T2],
        svc_type3: type[T3],
        svc_type4: type[T4],
        svc_type5: type[T5],
        /,
    ) -> tuple[T1, T2, T3, T4, T5]:
        ...

    @overload
    async def aget(
        self,
        svc_type1: type[T1],
        svc_type2: type[T2],
        svc_type3: type[T3],
        svc_type4: type[T4],
        svc_type5: type[T5],
        svc_type6: type[T6],
        /,
    ) -> tuple[T1, T2, T3, T4, T5, T6]:
        ...

    @overload
    async def aget(
        self,
        svc_type1: type[T1],
        svc_type2: type[T2],
        svc_type3: type[T3],
        svc_type4: type[T4],
        svc_type5: type[T5],
        svc_type6: type[T6],
        svc_type7: type[T7],
        /,
    ) -> tuple[T1, T2, T3, T4, T5, T6, T7]:
        ...

    @overload
    async def aget(
        self,
        svc_type1: type[T1],
        svc_type2: type[T2],
        svc_type3: type[T3],
        svc_type4: type[T4],
        svc_type5: type[T5],
        svc_type6: type[T6],
        svc_type7: type[T7],
        svc_type8: type[T8],
        /,
    ) -> tuple[T1, T2, T3, T4, T5, T6, T7, T8]:
        ...

    @overload
    async def aget(
        self,
        svc_type1: type[T1],
        svc_type2: type[T2],
        svc_type3: type[T3],
        svc_type4: type[T4],
        svc_type5: type[T5],
        svc_type6: type[T6],
        svc_type7: type[T7],
        svc_type8: type[T8],
        svc_type9: type[T9],
        /,
    ) -> tuple[T1, T2, T3, T4, T5, T6, T7, T8, T9]:
        ...

    @overload
    async def aget(
        self,
        svc_type1: type[T1],
        svc_type2: type[T2],
        svc_type3: type[T3],
        svc_type4: type[T4],
        svc_type5: type[T5],
        svc_type6: type[T6],
        svc_type7: type[T7],
        svc_type8: type[T8],
        svc_type9: type[T9],
        svc_type10: type[T10],
        /,
    ) -> tuple[T1, T2, T3, T4, T5, T6, T7, T8, T9, T10]:
        ...

    async def aget(self, *svc_types: type) -> object:
        """
        Get an instance of *svc_type*.

        Instantiate it asynchronously if necessary and register its cleanup.

        Returns:
             If one service is requested, it's returned directly. If multiple
             are requested, a sequence of services is returned.

        Note:
             See https://github.com/python/mypy/issues/4717 why this is
             necessary.
        """
        rv = []
        for svc_type in svc_types:
            if (svc := self._instantiated.get(svc_type)) is not None:
                rv.append(svc)
                continue

            rs = self.registry.get_registered_service_for(svc_type)
            svc = rs.factory()

            if isinstance(svc, AsyncGenerator):
                self._on_close.append((rs.name, svc))
                svc = await anext(svc)
            elif isawaitable(svc):
                svc = await svc

            self._instantiated[rs.svc_type] = svc

            rv.append(svc)

        if len(rv) == 1:
            return rv[0]

        return rv
