from ..types import Chain, Route, RouteOperationSwap, Token
from .mixins import SdkMixin


class DexHandler(SdkMixin):
    async def get_route(self, chain: Chain | str, token0: Token, token1: Token, amount: int) -> RouteOperationSwap:
        if isinstance(chain, str):
            chain = self.sdk.chains.find(chain)

        data = await self.api.dex.get_route(
            chain.chain_id,
            token0.contract_addr,
            token1.contract_addr,
            amount,
        )
        return RouteOperationSwap(**data)

    async def get_msg(
        self, chain: Chain | str, token0: Token, token1: Token, amount: int, slippage: float = 0.01
    ) -> object:
        if isinstance(chain, str):
            chain = self.sdk.chains.find(chain)

        return await self.api.dex.get_msg(
            chain.chain_id,
            token0.contract_addr,
            token1.contract_addr,
            amount,
            slippage,
        )
