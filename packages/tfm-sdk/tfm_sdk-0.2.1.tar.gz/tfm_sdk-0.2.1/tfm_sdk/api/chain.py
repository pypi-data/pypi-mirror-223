from .base import BaseAsyncAPI, BaseSyncAPI, api_url, sync_bind


class ChainApi(BaseAsyncAPI):
    async def get_chains(self, network_type: str | None = None, is_trading: bool | None = None) -> list:
        """Returns a list of supported source chains for swap.

        Args:
            network (str, optional): network type, mainnet or testnet. Defaults - all types.
            is_trading (bool, optional): chains with DEX. Defaults - False.

        Returns:
            list: list of chains.
        """
        return await self._get(api_url("chain"), params={"isTrading": is_trading, "networkType": network_type})

    async def get_tokens(
        self,
        chain_id: str,
        is_trading: bool | None = None,
        token_type: str | None = None,
    ):
        return await self._get(
            api_url("chain_tokens", chain_id=chain_id),
            params={"isTrading": is_trading, "tokenType": token_type},
        )

    async def get_token_info(self, chain_id: str, denom: str):
        return await self._get(api_url("chain_token_denom", chain_id=chain_id, denom=denom))


class ChainApiSync(BaseSyncAPI):
    @sync_bind(ChainApi.get_chains)
    def get_chains(self, network_type: str | None = None, is_trading: bool | None = None) -> list:
        pass

    get_chains.__doc__ = ChainApi.get_chains.__doc__

    @sync_bind(ChainApi.get_tokens)
    def get_tokens(
        self,
        chain_id: str,
        is_trading: bool | None = None,
        token_type: str | None = None,
    ):
        pass

    get_tokens.__doc__ = ChainApi.get_tokens.__doc__

    @sync_bind(ChainApi.get_token_info)
    def get_token_info(self, chain_id: str, denom: str):
        pass

    get_token_info.__doc__ = ChainApi.get_token_info.__doc__
