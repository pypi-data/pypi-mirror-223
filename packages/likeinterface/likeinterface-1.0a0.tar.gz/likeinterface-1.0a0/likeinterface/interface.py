from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, Optional

import httpx
from fastapi.requests import Request

from likeinterface.methods import LikeType, Method
from likeinterface.network import Network
from likeinterface.session import Session


class Interface:
    def __init__(
        self,
        network: Network,
        *,
        session: Optional[httpx.AsyncClient] = None,
        connect_kwargs: Dict[str, Any] = defaultdict(),  # noqa
    ) -> None:
        self.network = network
        self.session = Session(session=session, connect_kwargs=connect_kwargs)

    async def request(
        self,
        method: Method[LikeType],
        timeout: Optional[int] = None,
        fastapi_request: Optional[Request] = None,
    ) -> LikeType:
        return await self.session.request(
            interface=self,
            method=method,
            timeout=timeout,
            fastapi_request=fastapi_request,
        )
