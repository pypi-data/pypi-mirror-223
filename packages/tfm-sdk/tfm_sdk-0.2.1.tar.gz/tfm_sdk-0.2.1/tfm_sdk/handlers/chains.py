from ..types import Chain, NetworkType
from .mixins import SdkMixin


class ChainsHandler(SdkMixin):
    async def init(self):
        self.sdk.set_chains(await self.fetch_chains())

    async def fetch_chains(self) -> list[Chain]:
        data = await self.api.chain.get_chains()
        return [Chain(sdk=self.sdk, **row) for row in data]

    def get_list(self) -> list[Chain]:
        return self.chains

    def find(self, chain_name_or_id: str) -> Chain | None:
        for chain in self.chains:
            if chain.chain_id == chain_name_or_id or chain.chain_name == chain_name_or_id:
                return chain
        return None

    def filter_by_network_type(self, network_type: NetworkType) -> list[Chain]:
        return [chain for chain in self.chains if chain.network_type == network_type]

    def mainnet_only(self) -> list[Chain]:
        return self.filter_by_network_type(NetworkType.MAINNET)

    def testnet_only(self) -> list[Chain]:
        return self.filter_by_network_type(NetworkType.TESTNET)

    async def get_reachable(self, chain: Chain | str) -> list[Chain]:
        if isinstance(chain, Chain):
            chain = chain.chain_id

        data = await self.api.ibc.chain.get_reachable(chain)
        return [Chain(sdk=self.sdk, **item) for item in data]

    async def is_reachable(self, source_chain: Chain | str, destination_chain: Chain | str) -> bool:
        if isinstance(source_chain, Chain):
            source_chain = source_chain.chain_id

        if isinstance(destination_chain, Chain):
            destination_chain = destination_chain.chain_id

        data = await self.api.ibc.chain.is_reachable(source_chain, destination_chain)
        return data["reachable"]
