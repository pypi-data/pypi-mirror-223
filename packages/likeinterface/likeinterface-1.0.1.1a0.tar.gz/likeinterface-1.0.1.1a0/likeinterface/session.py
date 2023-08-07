from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Dict, Optional, cast

import httpx

from likeinterface.constants import REQUEST_TIMEOUT
from likeinterface.exceptions import LikeNetworkError
from likeinterface.methods import LikeType, Method
from likeinterface.utils.response_validator import response_validator

if TYPE_CHECKING:
    from likeinterface.interface import Interface


class SessionManager:
    def __init__(
        self,
        session: Optional[httpx.AsyncClient] = None,
        *,
        connect_kwargs: Dict[str, Any] = defaultdict(),  # noqa
    ) -> None:
        self.session = session
        self.connect_kwargs = connect_kwargs
        self.should_reset_connector = not self.session

    async def create(self) -> None:
        if self.should_reset_connector:
            await self.close()
        if self.session is None or self.session.is_closed:
            self.session = httpx.AsyncClient(**self.connect_kwargs)
            self.should_reset_connector = False

    async def close(self) -> None:
        if self.session and not self.session.is_closed:
            await self.session.aclose()


class Session(SessionManager):
    def __init__(
        self,
        *,
        session: Optional[httpx.AsyncClient] = None,
        connect_kwargs: Dict[str, Any] = defaultdict(),  # noqa
    ) -> None:
        super(Session, self).__init__(
            session=session,
            connect_kwargs=connect_kwargs,
        )

    async def request(
        self, interface: Interface, method: Method[LikeType], timeout: Optional[int] = None
    ) -> LikeType:
        await self.create()

        request = method.request(interface=interface)

        try:
            response = await self.session.post(  # type: ignore[union-attr]
                url=interface.network.url(method=method.__name__),
                json=request.data,
                timeout=REQUEST_TIMEOUT if not timeout else timeout,
            )
        except asyncio.TimeoutError:
            raise LikeNetworkError("Exception %s: %s." % (method, "request timeout error"))
        except httpx.NetworkError as e:
            raise LikeNetworkError(
                "Exception for method %s: %s." % (method.__name__, f"{type(e).__name__}: {e}")
            )

        response = response_validator(
            method=method, status_code=response.status_code, content=response.text
        )
        return cast(LikeType, response.result)
