from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Dict, Optional, cast

import httpx
from fastapi.requests import Request

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
        self,
        interface: Interface,
        method: Method[LikeType],
        timeout: Optional[int] = None,
        fastapi_request: Optional[Request] = None,
    ) -> LikeType:
        await self.create()

        request = method.request(interface=interface)

        if fastapi_request:
            json = await fastapi_request.json()

            if isinstance(json, Dict):
                request.data |= json

        try:
            response = await self.session.post(  # type: ignore[union-attr]
                url=interface.network.url(method=method.__name__),
                json=request.data,
                params=fastapi_request.query_params if fastapi_request else None,
                headers=fastapi_request.headers if fastapi_request else None,
                cookies=fastapi_request.cookies if fastapi_request else None,
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
