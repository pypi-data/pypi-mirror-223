from __future__ import annotations

import math
import sys
from typing import TYPE_CHECKING, Generic, TypeVar

from anyio import WouldBlock, create_memory_object_stream, create_task_group, fail_after
from anyio.streams.memory import BrokenResourceError, ClosedResourceError, EndOfStream

from async_wrapper.exception import QueueBrokenError, QueueEmptyError, QueueFullError

if sys.version_info < (3, 11):
    from exceptiongroup import ExceptionGroup  # type: ignore

if TYPE_CHECKING:
    from types import TracebackType

    from anyio.streams.memory import (
        MemoryObjectReceiveStream,
        MemoryObjectSendStream,
        MemoryObjectStreamStatistics,
    )
    from typing_extensions import Self

__all__ = ["Queue"]

ValueT = TypeVar("ValueT")


class Queue(Generic[ValueT]):
    """obtained from asyncio.Queue"""

    _setter: MemoryObjectSendStream[ValueT]
    _getter: MemoryObjectReceiveStream[ValueT]

    def __init__(
        self,
        max_size: float | None = None,
        stream: tuple[MemoryObjectSendStream[ValueT], MemoryObjectReceiveStream[ValueT]]
        | None = None,
    ) -> None:
        if stream is None:
            self._setter, self._getter = create_memory_object_stream(
                max_buffer_size=max_size or math.inf,
            )
        else:
            setter, getter = stream
            if setter._closed or getter._closed:  # noqa: SLF001
                raise QueueBrokenError("setter or getter is closed")
            if setter._state.buffer is not getter._state.buffer:  # noqa: SLF001
                raise QueueBrokenError("setter and getter has diff buffer.")
            self._setter, self._getter = stream

    @property
    def _closed(self) -> bool:
        return self._setter._closed or self._getter._closed  # noqa: SLF001

    def qsize(self) -> int:
        """number of items in the queue."""
        return len(self._getter._state.buffer)  # noqa: SLF001

    @property
    def maxsize(self) -> float:
        """number of items allowed in the queue."""
        return self._getter._state.max_buffer_size  # noqa: SLF001

    def empty(self) -> bool:
        """true if the queue is empty, false otherwise."""
        return self.qsize() <= 0

    def full(self) -> bool:
        """return true if there are maxsize items in the queue."""
        if self.maxsize == math.inf:
            return False
        return self.qsize() >= self.maxsize

    async def aget(self, *, timeout: float | None = None) -> ValueT:
        """remove and return an item from the queue.

        Args:
            timeout: error occurs when over timeout. Defaults to None.

        Returns:
            item from queue
        """
        with fail_after(timeout):
            return await self._aget()

    async def aput(self, value: ValueT, *, timeout: float | None = None) -> None:
        """put an item into the queue.

        Args:
            value: item
            timeout: error occurs when over timeout. Defaults to None.
        """
        with fail_after(timeout):
            await self._aput(value)

    async def _aget(self) -> ValueT:
        """remove and return an item from the queue."""
        try:
            return await self._getter.receive()
        except WouldBlock as exc:
            raise QueueEmptyError from exc
        except (ClosedResourceError, BrokenResourceError) as exc:
            raise QueueBrokenError from exc

    async def _aput(self, value: ValueT) -> None:
        """put an item into the queue."""
        try:
            await self._setter.send(value)
        except WouldBlock as exc:
            raise QueueFullError from exc
        except (ClosedResourceError, BrokenResourceError) as exc:
            raise QueueBrokenError from exc

    def get(self) -> ValueT:
        """remove and return an item from the queue without blocking."""
        try:
            return self._getter.receive_nowait()
        except WouldBlock as exc:
            raise QueueEmptyError from exc
        except (ClosedResourceError, BrokenResourceError) as exc:
            raise QueueBrokenError from exc

    def put(self, value: ValueT) -> None:
        """put an item into the queue without blocking."""
        try:
            self._setter.send_nowait(value)
        except WouldBlock as exc:
            raise QueueFullError from exc
        except (ClosedResourceError, BrokenResourceError) as exc:
            raise QueueBrokenError from exc

    async def aclose(self) -> None:
        """close the stream as async"""
        try:
            await self._aclose()
        except (ClosedResourceError, BrokenResourceError) as exc:
            raise QueueBrokenError from exc
        except ExceptionGroup as exc:
            if all(
                isinstance(error, (ClosedResourceError, BrokenResourceError))
                for error in exc.exceptions
            ):
                raise QueueBrokenError from exc
            raise

    def close(self) -> None:
        """close the stream as sync"""
        try:
            self._close()
        except (ClosedResourceError, BrokenResourceError) as exc:
            raise QueueBrokenError from exc

    async def _aclose(self) -> None:
        """close the stream as async"""
        async with create_task_group() as task_group:
            task_group.start_soon(self._getter.aclose)
            task_group.start_soon(self._setter.aclose)

    def _close(self) -> None:
        """close the stream as sync"""
        self._getter.close()
        self._setter.close()

    def clone(self, *, setter: bool = False, getter: bool = False) -> Queue[ValueT]:
        """create clone of this queue.

        Args:
            setter: if true, clone setter. Defaults to False.
            getter: if true, clone getter. Defaults to False.

        Returns:
            clone
        """
        try:
            return self._clone(setter=setter, getter=getter)
        except (ClosedResourceError, BrokenResourceError) as exc:
            raise QueueBrokenError from exc

    def _clone(self, *, setter: bool, getter: bool) -> Queue[ValueT]:
        """create clone of this queue"""
        if self._closed:
            raise QueueBrokenError("the queue is already closed")
        if not setter and not getter:
            raise ValueError("setter and getter are None.")
        _setter = self._setter.clone() if setter else self._setter
        _getter = self._getter.clone() if getter else self._getter
        return Queue(stream=(_setter, _getter))

    def statistics(self) -> MemoryObjectStreamStatistics:
        """return statstics from stream"""
        return self._getter._state.statistics()  # noqa: SLF001

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    def __aiter__(self) -> Self:
        return self

    async def __anext__(self) -> ValueT:
        try:
            return await self.aget()
        except (EndOfStream, QueueEmptyError, QueueBrokenError) as exc:
            raise StopAsyncIteration from exc

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> ValueT:
        try:
            return self.get()
        except (EndOfStream, QueueEmptyError, QueueBrokenError) as exc:
            raise StopIteration from exc
