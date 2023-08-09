from ..base import BaseAsyncAPI, BaseSyncAPI, api_url, sync_bind


class IbcChainApi(BaseAsyncAPI):
    async def get_reachable(self, chain_id: str):
        """Returns a list of supported destination chains for swap.

        Args:
            chain_id (str): source chain id.

        Returns:
            list: list of chains.
        """
        return await self._get(api_url("chain_reachable", chain_id=chain_id))

    async def is_reachable(self, source_chain_id: str, destination_chain_id: str):
        return await self._get(
            api_url("chain_is_reachable", source_chain_id=source_chain_id, destination_chain_id=destination_chain_id)
        )

    async def get_transferable_tokens(self, source_chain_id: str, destination_chain_id: str):
        """Returns a list of supported tokens for swap.

        Args:
            source_chain_id (str): source chain id.
            destination_chain_id (str): destination chain id.

        Returns:
            list: A list of dictionaries containing source_token and destination_token keys.
        """
        return await self._get(
            api_url(
                "chain_transferable_tokens", source_chain_id=source_chain_id, destination_chain_id=destination_chain_id
            )
        )

    async def is_token_transferable(self, source_chain_id: str, destination_chain_id: str, denom: str):
        return await self._get(
            api_url(
                "chain_is_token_transferable",
                source_chain_id=source_chain_id,
                destination_chain_id=destination_chain_id,
                denom=denom,
            )
        )


class IbcChainApiSync(BaseSyncAPI):
    @sync_bind(IbcChainApi.get_reachable)
    def get_reachable(self, chain_id: str):
        pass

    get_reachable.__doc__ = IbcChainApi.get_reachable.__doc__

    @sync_bind(IbcChainApi.is_reachable)
    def is_reachable(self, source_chain_id: str, destination_chain_id: str):
        pass

    is_reachable.__doc__ = IbcChainApi.is_reachable.__doc__

    @sync_bind(IbcChainApi.get_transferable_tokens)
    def get_transferable_tokens(self, source_chain_id: str, destination_chain_id: str):
        pass

    get_transferable_tokens.__doc__ = IbcChainApi.get_transferable_tokens.__doc__

    @sync_bind(IbcChainApi.is_token_transferable)
    def is_token_transferable(self, source_chain_id: str, destination_chain_id: str, denom: str):
        pass

    is_token_transferable.__doc__ = IbcChainApi.is_token_transferable.__doc__
