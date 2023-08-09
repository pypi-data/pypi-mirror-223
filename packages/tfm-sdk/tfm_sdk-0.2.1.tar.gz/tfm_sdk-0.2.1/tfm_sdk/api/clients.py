from dataclasses import dataclass

from .base import BaseAsyncAPI, BaseSyncAPI, sync_bind
from .chain import ChainApi, ChainApiSync
from .dex import DexApi, DexApiSync
from .ibc import IbcChainApi, IbcChainApiSync, IbcSwapApi, IbcSwapApiSync, IbcTransferApi, IbcTransferApiSync
from .price import PriceApi, PriceApiSync


@dataclass
class IbcApi:
    chain: IbcChainApi
    transfer: IbcTransferApi
    swap: IbcSwapApi


class TfmApi(BaseAsyncAPI):
    """
    Low-level asynchronous API interface for TFM.
    """

    ibc: IbcApi
    chain: ChainApi
    price: PriceApi
    dex: DexApi

    def __init__(self, loop=None, base_url=None, session=None, **kwargs):
        super().__init__(loop=loop, base_url=base_url, session=session, **kwargs)
        session = self.get_session()

        self.ibc = IbcApi(
            chain=IbcChainApi(loop=loop, base_url=base_url, session=session, **kwargs),
            transfer=IbcTransferApi(loop=loop, base_url=base_url, session=session, **kwargs),
            swap=IbcSwapApi(loop=loop, base_url=base_url, session=session, **kwargs),
        )
        self.chain = ChainApi(loop=loop, base_url=base_url, session=session, **kwargs)
        self.price = PriceApi(loop=loop, base_url=base_url, session=session, **kwargs)
        self.dex = DexApi(loop=loop, base_url=base_url, session=session, **kwargs)

    async def health(self):
        try:
            text = await self._get("/health", content="text")
            return "UP" in text
        except Exception:
            return False


@dataclass
class IbcApiSync:
    chain: IbcChainApiSync
    transfer: IbcTransferApiSync
    swap: IbcSwapApiSync


class TfmApiSync(BaseSyncAPI):
    ibc: IbcApiSync
    chain: ChainApiSync
    price: PriceApiSync
    dex: DexApiSync

    def __init__(self, loop=None, base_url=None, session=None, **kwargs):
        super().__init__(loop=loop, base_url=base_url, session=session, **kwargs)
        session = self.get_session()

        self.ibc = IbcApiSync(
            chain=IbcChainApiSync(loop=loop, base_url=base_url, session=session, **kwargs),
            transfer=IbcTransferApiSync(loop=loop, base_url=base_url, session=session, **kwargs),
            swap=IbcSwapApiSync(loop=loop, base_url=base_url, session=session, **kwargs),
        )
        self.chain = ChainApiSync(loop=loop, base_url=base_url, session=session, **kwargs)
        self.price = PriceApiSync(loop=loop, base_url=base_url, session=session, **kwargs)
        self.dex = DexApiSync(loop=loop, base_url=base_url, session=session, **kwargs)

    @sync_bind(TfmApi.health)
    def health(self):
        pass

    health.__doc__ = TfmApi.health.__doc__
