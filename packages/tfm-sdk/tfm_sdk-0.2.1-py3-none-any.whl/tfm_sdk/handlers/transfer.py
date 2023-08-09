from ..types import Chain, IbcTransferSwap, Route, RouteAndMsgs, SwapPair
from .mixins import SdkMixin


class TransferHandler(SdkMixin):
    async def get_transferable_tokens(self) -> list[SwapPair]:
        data = await self.api.ibc.chain.get_transferable_tokens(
            self.source_chain.chain_id, self.destination_chain.chain_id
        )
        return [
            SwapPair(source_chain=self.source_chain, destination_chain=self.destination_chain, **item) for item in data
        ]

    async def is_token_transferable(
        self, denom: str, source_chain: Chain | None = None, destination_chain: Chain | None = None
    ) -> bool:
        source_chain = source_chain or self.source_chain
        destination_chain = destination_chain or self.destination_chain
        data = await self.api.ibc.chain.is_token_transferable(source_chain.chain_id, destination_chain.chain_id, denom)
        return data["transferable"]

    async def get_route(self, swap_pair: SwapPair, amount: int) -> Route:
        data = await self.api.ibc.transfer.get_route(
            swap_pair.source_token.contract_addr,
            self.source_chain.chain_id,
            swap_pair.destination_token.contract_addr,
            self.destination_chain.chain_id,
            amount,
        )
        return Route(**data)

    async def get_msg(
        self, swap_pair: SwapPair, amount: int, slippage: float = 0.01, pfm_enabled: bool | None = None
    ) -> list[IbcTransferSwap]:
        data = await self.api.ibc.transfer.get_msg(
            swap_pair.source_token.contract_addr,
            self.source_chain.chain_id,
            swap_pair.destination_token.contract_addr,
            self.destination_chain.chain_id,
            amount,
            slippage,
            pfm_enabled,
        )
        return [IbcTransferSwap(**row) for row in data]

    async def get_route_swap(
        self, swap_pair: SwapPair, amount: int, slippage: float = 0.01, pfm_enabled=True
    ) -> RouteAndMsgs:
        data = await self.api.ibc.transfer.get_route_msg_combined(
            swap_pair.source_token.contract_addr,
            self.source_chain.chain_id,
            swap_pair.destination_token.contract_addr,
            self.destination_chain.chain_id,
            amount,
            slippage,
            pfm_enabled,
        )
        return RouteAndMsgs(**data)
