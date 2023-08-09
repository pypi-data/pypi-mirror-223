from .api import TfmApi
from .exceptions import TfmSdkException
from .handlers import ChainsHandler, DexHandler, SwapsHandler, TokensHandler, TransferHandler
from .types import Chain


class TfmSdk:
    def __init__(self, api: TfmApi | None = None):
        self.api: TfmApi = api or TfmApi()
        self.is_initialized: bool = False
        self._chains_list: list[Chain] = []
        self.source_chain: Chain | None = None
        self.destination_chain: Chain | None = None

        self.chains = ChainsHandler(self)
        self.transfer = TransferHandler(self)
        self.tokens = TokensHandler(self)
        self.swap = SwapsHandler(self)
        self.dex = DexHandler(self)

    async def is_api_online(self) -> bool:
        return await self.api.health()

    async def init(self):
        await self.chains.init()
        self.is_initialized = True

    def get_chains(self) -> list[Chain]:
        self._check_initialized()
        return self._chains_list

    def set_chains(self, chains):
        self._chains_list = chains

    def set_source_chain(self, chain: Chain):
        self.source_chain = chain
        return self

    def set_destination_chain(self, chain: Chain):
        self.destination_chain = chain
        return self

    def reverse(self):
        self.source_chain, self.destination_chain = self.destination_chain, self.source_chain
        return self

    def _check_initialized(self):
        if not self.is_initialized:
            raise TfmSdkException("SDK not initialized. Call `await sdk.init()` first or use `async with sdk:`.")

    async def validate(self):
        self._check_initialized()

        if self.source_chain is None:
            raise TfmSdkException("Source chain is not set")

        if self.destination_chain is None:
            raise TfmSdkException("Destination chain is not set")

        if self.source_chain.chain_id == self.destination_chain.chain_id:
            raise TfmSdkException("Source chain and destination chain cannot be the same")

    async def __aenter__(self):
        await self.init()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self):
        await self.api.close_session()
