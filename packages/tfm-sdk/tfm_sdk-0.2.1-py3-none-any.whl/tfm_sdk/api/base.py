import asyncio
import logging
from asyncio import get_event_loop
from typing import Union

import aiohttp
import wrapt
from yarl import URL

from ..config import BASE_API_URL
from .exceptions import TfmApiException

logging.basicConfig(level=logging.DEBUG)


VERSION = "v1"
API_ENDPOINTS = {
    # price
    "price": "/price/{chain_id}/{denom}",
    # dex
    "dex_route": "/dex-aggregator/route/{chain_id}/{source_denom}/{destination_denom}/{amount}",
    "dex_msg": "/dex-aggregator/msg/{chain_id}/{source_denom}/{destination_denom}/{amount}",
    # chains
    "chain_tokens": "/ibc/chain/{chain_id}/tokens",
    "chain_token_denom": "/ibc/chain/{chain_id}/token/{denom}",
    # ibc chain
    "chain": "/ibc/chain",
    "chain_reachable": "/ibc/chain/{chain_id}/reachable-chains",
    "chain_is_reachable": "/ibc/chain/{source_chain_id}/reachable-chain/{destination_chain_id}",
    "chain_transferable_tokens": "/ibc/chain/{source_chain_id}/transferable-tokens/{destination_chain_id}",
    "chain_is_token_transferable": "/ibc/chain/{source_chain_id}/transferable-token/{destination_chain_id}/{denom}",
    # transfer
    "transfer_route": "/ibc/transfer/route/{chain0}/{chain1}/{token0}/{token1}/{amount}",
    "transfer_msg": "/ibc/transfer/msg/{chain0}/{chain1}/{token0}/{token1}/{amount}",
    "transfer_route_msg_combined": "/ibc/transfer/route-msg-combined/{chain0}/{chain1}/{token0}/{token1}/{amount}",
    # swap
    "swap_route": "/ibc/swap/route/{chain0}/{chain1}/{token0}/{token1}/{amount}",
    "swap_msg": "/ibc/swap/msg/{chain0}/{chain1}/{token0}/{token1}/{amount}",
    "swap_route_msg_combined": "/ibc/swap/route-msg-combined/{chain0}/{chain1}/{token0}/{token1}/{amount}",
}


def api_url(endpoint: str, **kwargs):
    endpoint = API_ENDPOINTS[endpoint]
    if kwargs:
        for key, value in kwargs.items():
            if isinstance(value, str) and value.startswith("ibc/"):
                kwargs[key] = "ibc%%2F%s" % value[4:]
        endpoint = endpoint.format(**kwargs)

    return f"/api/{VERSION}{endpoint}"


class BaseAsyncAPI:
    sync = False

    def __init__(self, loop=None, base_url=None, session=None, **kwargs):
        self.loop = loop or get_event_loop()
        self.base_url = base_url or URL(BASE_API_URL)

        self._session = session or self.create_session(**kwargs)

    def create_session(self, **kwargs):
        return aiohttp.ClientSession(loop=self.loop, base_url=self.base_url, **kwargs)

    def get_session(self):
        if self._session:
            return self._session
        return self.create_session()

    async def close_session(self):
        if self._session:
            await self._session.close()

    async def _get(self, endpoint: str, params=None, content="json"):
        async with self.get_session().get(endpoint, params=self._prepare_params(params)) as r:
            try:
                assert r.ok, endpoint
                if content == "text":
                    return await r.text()
                else:
                    return await r.json()
            except (AssertionError, aiohttp.client_exceptions.ContentTypeError):
                raise TfmApiException(r)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close_session()

    @staticmethod
    def _prepare_params(params: Union[dict, None] = None) -> dict:
        """Prepares the parameters for the API call."""
        if not params:
            return {}

        filtered_params = {}
        for k, v in params.items():
            if v is None:
                continue

            elif isinstance(v, (list, tuple)):
                filtered_params[k] = ",".join([str(i).strip() for i in v])
            elif isinstance(v, bool):
                filtered_params[k] = str(v).lower()
            else:
                filtered_params[k] = str(v).strip()
                if k == "networkType":
                    filtered_params[k] = filtered_params[k].lower()

        return filtered_params


class BaseSyncAPI(BaseAsyncAPI):
    sync = True

    def _run_sync(self, coroutine, loop=None):
        """Runs an asynchronous coroutine synchronously."""
        if not loop:
            loop = asyncio.new_event_loop()
        return loop.run_until_complete(coroutine)

    def __del__(self):
        if self._session:
            try:
                self.loop.run_until_complete(self._session.close())
            except RuntimeError:
                pass


def sync_bind(async_call):
    """A decorator that redirects the function to the synchronous version of async_call."""

    @wrapt.decorator
    def decorator(wrapped, instance, args, kwargs):
        return instance._run_sync(async_call(instance, *args, **kwargs), loop=instance.loop)

    return decorator
