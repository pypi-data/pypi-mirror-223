from ..exceptions import TfmSdkException
from ..types import Chain, Token, TokenType
from .mixins import SdkMixin


class TokensHandler(SdkMixin):
    async def get_for_chain(
        self,
        chain: Chain | str,
        is_trading: bool | None = None,
        token_type: TokenType | str | None = None,
    ) -> list[Token]:
        if isinstance(chain, str):
            chain = self.sdk.chains.find(chain)
            assert chain is not None

        if isinstance(token_type, TokenType):
            token_type = token_type.value

        data = await self.api.chain.get_tokens(chain.chain_id, is_trading, token_type)
        return [Token(chain=chain, sdk=self.sdk, **token) for token in data]

    async def get_by_symbol(self, chain: Chain | str, symbol: str) -> Token:
        tokens = await self.get_for_chain(chain)
        for token in tokens:
            if token.symbol == symbol.upper():
                return token

    async def get_info(
        self,
        chain: Chain | str,
        contract_addr: str,
    ) -> Token | None:
        if isinstance(chain, str):
            chain = self.sdk.chains.find(chain)

        data = await self.api.chain.get_token_info(chain.chain_id, contract_addr)
        if not data:
            return None

        return Token(chain=chain, sdk=self.sdk, **data)

    async def get_price(self, token: Token, timestamp: int | None = None) -> float:
        data = await self.api.price.get_price(token.chain.chain_id, token.contract_addr, timestamp)
        return data["price"]
