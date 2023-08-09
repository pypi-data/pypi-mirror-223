from .base import BaseAsyncAPI, BaseSyncAPI, api_url, sync_bind


class PriceApi(BaseAsyncAPI):
    async def get_price(self, chain_id: str, denom: str, timestamp: int | None = None):
        """Returns the price of a token.

        Args:
            chain_id (str): chain id.
            denom (str): token denom.
            timestamp (int, optional): timestamp. Defaults to None.
        Returns:
            dict: A dictionary containing price and timestamp keys.
        """
        return await self._get(api_url("price", chain_id=chain_id, denom=denom), params={"timestamp": timestamp})


class PriceApiSync(BaseSyncAPI):
    @sync_bind(PriceApi.get_price)
    def get_price(self, chain_id: str, denom: str, timestamp: int | None = None):
        pass

    get_price.__doc__ = PriceApi.get_price.__doc__
