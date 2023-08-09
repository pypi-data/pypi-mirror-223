from ..base import BaseAsyncAPI, BaseSyncAPI, api_url, sync_bind


class IbcTransferApi(BaseAsyncAPI):
    async def get_route(self, token0: str, chain0: str, token1: str, chain1: str, amount: int):
        return await self._get(
            api_url("transfer_route", token0=token0, chain0=chain0, token1=token1, chain1=chain1, amount=amount)
        )

    async def get_msg(
        self,
        token0: str,
        chain0: str,
        token1: str,
        chain1: str,
        amount: int,
        slippage: float,
        pfm_enabled=None,
    ):
        return await self._get(
            api_url("transfer_msg", token0=token0, chain0=chain0, token1=token1, chain1=chain1, amount=amount),
            params={"slippage": str(slippage), "pfmEnabled": pfm_enabled},
        )

    async def get_route_msg_combined(
        self,
        token0: str,
        chain0: str,
        token1: str,
        chain1: str,
        amount: int,
        slippage: float,
        pfm_enabled=True,
    ):
        """Get route and swap message cross chains

        Args:
            token0 (str): source token address
            chain0 (str): source token chain id
            token1 (str): destination token address
            chain1 (str): destination chain id
            amount (int): amount of token0
            slippage (float): slippage of swap, ex. 0.05 = 5% slippage
            pfm_enabled (bool, optional): When true, returns only the chains that have PFM enabled. Defaults to True.

        Returns:
            dict: route and swap keys in dict
        """
        return await self._get(
            api_url(
                "transfer_route_msg_combined", token0=token0, chain0=chain0, token1=token1, chain1=chain1, amount=amount
            ),
            params={
                "slippage": str(slippage),
                "pfmEnabled": pfm_enabled,
            },
        )


class IbcTransferApiSync(BaseSyncAPI):
    @sync_bind(IbcTransferApi.get_route)
    def get_route(self, token0: str, chain0: str, token1: str, chain1: str, amount: int):
        pass

    get_route.__doc__ = IbcTransferApi.get_route.__doc__

    @sync_bind(IbcTransferApi.get_msg)
    def get_msg(
        self,
        token0: str,
        chain0: str,
        token1: str,
        chain1: str,
        amount: int,
        slippage: float,
        pfm_enabled=None,
    ):
        pass

    get_msg.__doc__ = IbcTransferApi.get_msg.__doc__

    @sync_bind(IbcTransferApi.get_route_msg_combined)
    def get_route_msg_combined(
        self,
        token0: str,
        chain0: str,
        token1: str,
        chain1: str,
        amount: int,
        slippage: float,
        pfm_enabled=True,
    ):
        pass

    get_route_msg_combined.__doc__ = IbcTransferApi.get_route_msg_combined.__doc__
