from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Dict, Optional, cast

from aiohttp.client import ClientError, ClientSession

from likeinterface.constants import REQUEST_TIMEOUT
from likeinterface.exceptions import LikeNetworkError
from likeinterface.methods import LikeType, Method
from likeinterface.utils.response_validator import response_validator

if TYPE_CHECKING:
    from likeinterface.interface import Interface


class SessionManager:
    def __init__(
        self,
        session: Optional[ClientSession] = None,
        *,
        connect_kwargs: Dict[str, Any] = defaultdict(),  # noqa
    ) -> None:
        self.session = session
        self.connect_kwargs = connect_kwargs
        self.should_reset_connector = not self.session

    async def create(self) -> None:
        if self.should_reset_connector:
            await self.close()
        if self.session is None or self.session.closed:
            self.session = ClientSession(**self.connect_kwargs)
            self.should_reset_connector = False

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()


class Session(SessionManager):
    def __init__(
        self,
        *,
        session: Optional[ClientSession] = None,
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
            async with self.session.post(
                url=interface.network.url(method=method.__name__),
                json=request.data,
                timeout=REQUEST_TIMEOUT if not timeout else timeout,
            ) as response:
                content = await response.text()
        except asyncio.TimeoutError:
            raise LikeNetworkError("Exception %s: %s." % (method, "request timeout error"))
        except ClientError as e:
            raise LikeNetworkError(
                "Exception for method %s: %s." % (method.__name__, f"{type(e).__name__}: {e}")
            )

        response = response_validator(method=method, status_code=response.status, content=content)
        return cast(LikeType, response.result)
