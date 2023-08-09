from .base import BaseAsyncAPI, BaseSyncAPI, api_url, sync_bind


class DexApi(BaseAsyncAPI):
    async def get_route(self, chain_id: str, source_denom: str, destination_denom: str, amount: int):
        """Returns the route for a swap.

        Args:
            chain_id (str): chain id.
            source_denom (str): source_denom denom.
            destination_denom (str): destination_denom denom.
            amount (int): amount of source_denom to swap.
        Returns:
            dict: A dictionary containing the route.
        """
        return await self._get(
            api_url(
                "dex_route",
                chain_id=chain_id,
                source_denom=source_denom,
                destination_denom=destination_denom,
                amount=amount,
            )
        )

    async def get_msg(
        self, chain_id: str, source_denom: str, destination_denom: str, amount: int, slippage: float = 0.01
    ):
        """Returns the message for a swap.

        Args:
            chain_id (str): chain id.
            source_denom (str): source_denom denom.
            destination_denom (str): destination_denom denom.
            amount (int): amount of source_denom to swap.
            slippage (float, optional): slippage. Defaults to 0.01.
        Returns:
            dict: A dictionary containing the message.
        """
        return await self._get(
            api_url(
                "dex_msg",
                chain_id=chain_id,
                source_denom=source_denom,
                destination_denom=destination_denom,
                amount=amount,
            ),
            params={"slippage": slippage},
        )


class DexApiSync(BaseSyncAPI):
    @sync_bind(DexApi.get_route)
    def get_route(self, chain_id: str, source_denom: str, destination_denom: str, amount: int):
        pass

    get_route.__doc__ = DexApi.get_route.__doc__

    @sync_bind(DexApi.get_msg)
    def get_msg(self, chain_id: str, source_denom: str, destination_denom: str, amount: int, slippage: float = 0.01):
        pass

    get_msg.__doc__ = DexApi.get_msg.__doc__
