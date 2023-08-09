from ..types import IbcTransferSwap, Route, RouteAndMsgs, Swap, SwapMode, SwapPair, SwapType
from .mixins import SdkMixin


class SwapsHandler(SdkMixin):
    async def get_route(self, swap_pair: SwapPair, amount: int, swap_mode: SwapMode = SwapMode.TURBO) -> Route:
        data = await self.api.ibc.swap.get_route(
            swap_pair.source_token.contract_addr,
            self.source_chain.chain_id,
            swap_pair.destination_token.contract_addr,
            self.destination_chain.chain_id,
            amount,
            swap_mode=swap_mode,
        )
        return Route(**data)

    async def get_msg(
        self,
        swap_pair: SwapPair,
        amount: int,
        slippage: float = 0.01,
        pfm_enabled: bool | None = None,
        swap_mode="Turbo",
    ) -> list[Swap]:
        data = await self.api.ibc.swap.get_msg(
            swap_pair.source_token.contract_addr,
            self.source_chain.chain_id,
            swap_pair.destination_token.contract_addr,
            self.destination_chain.chain_id,
            amount,
            slippage,
            pfm_enabled,
            swap_mode=swap_mode,
        )
        return [Swap(**row) if row["type"] == SwapType.SWAP.value else IbcTransferSwap(**row) for row in data]

    async def get_route_swap(
        self, swap_pair: SwapPair, amount: int, slippage: float, pfm_enabled=True, swap_mode: SwapMode = SwapMode.TURBO
    ) -> RouteAndMsgs:
        data = await self.api.ibc.swap.get_route_msg_combined(
            swap_pair.source_token.contract_addr,
            self.source_chain.chain_id,
            swap_pair.destination_token.contract_addr,
            self.destination_chain.chain_id,
            amount,
            slippage,
            pfm_enabled,
            swap_mode=swap_mode,
        )
        return RouteAndMsgs(**data)
