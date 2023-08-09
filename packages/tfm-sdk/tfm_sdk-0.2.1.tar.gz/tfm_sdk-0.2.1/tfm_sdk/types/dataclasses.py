from dataclasses import dataclass

from .enums import NetworkType, RouteOperationType, SwapType
from .mixins import UnderscoreOrCamelCaseMeta
from .utils import get_or


@dataclass(init=False)
class Chain(UnderscoreOrCamelCaseMeta):
    id: int
    chain_name: str
    pretty_name: str
    chain_id: str
    network_type: NetworkType
    status: str
    github_url: str
    is_trading: bool
    image_url: str
    is_pfm_enabled: bool | None
    is_wasm_hook_enabled: bool | None

    async def get_tokens(self, is_trading: bool | None = None, token_type: str | None = None) -> list:
        return await self.sdk.tokens.get_for_chain(self, is_trading, token_type)

    async def get_token_by_denom(self, denom: str):
        return await self.sdk.tokens.get_info(self, contract_addr=denom)

    async def get_reachable(self):
        return await self.sdk.chains.get_reachable(self)


@dataclass(init=False)
class Token(UnderscoreOrCamelCaseMeta):
    name: str
    symbol: str
    contract_addr: str
    decimals: int
    image_url: str | None
    number_of_pools: int
    chain: Chain
    is_trading: bool

    async def get_price(self, timestamp: int | None = None) -> float:
        return await self.sdk.tokens.get_price(self, timestamp)


@dataclass(init=False)
class SwapPair:
    source_chain: Chain
    destination_chain: Chain
    source_token: Token
    destination_token: Token

    def __init__(self, sdk=None, **kwargs):
        self.sdk = sdk
        self.source_chain = get_or(kwargs, "source_chain", "sourceChain", required=False)
        self.destination_chain = get_or(kwargs, "destination_chain", "destinationChain", required=False)

        source_token = get_or(kwargs, "source_token", "sourceToken")
        destination_token = get_or(kwargs, "destination_token", "destinationToken")
        self.source_token = (
            Token(chain=self.source_chain, **source_token) if isinstance(source_token, dict) else source_token
        )
        self.destination_token = (
            Token(chain=self.destination_chain, **destination_token)
            if isinstance(destination_token, dict)
            else destination_token
        )

    async def is_transferable(self) -> bool:
        return await self.sdk.transfer.is_token_transferable(
            self.source_token.contract_addr,
            source_chain=self.source_chain,
            destination_chain=self.destination_chain,
        )


@dataclass(init=False)
class ChainSwapOperation(UnderscoreOrCamelCaseMeta):
    offer_token: str
    offer_chain: str
    ask_token: str
    ask_chain: str
    exchange: str
    pool_id: str | None
    contract_addr: str


@dataclass(init=False)
class ChainSwapRoute(UnderscoreOrCamelCaseMeta):
    input_amount: int
    return_amount: int
    price_impact: float
    input_percent: int
    operations: list[ChainSwapOperation]


@dataclass(init=False)
class RouteOperation(UnderscoreOrCamelCaseMeta):
    type: RouteOperationType
    input_amount: int
    return_amount: int


@dataclass
class RouteOperationSwap(RouteOperation):
    price_impact: float
    chain_name: str
    chain_id: str
    routes: list[ChainSwapRoute]
    alternatives: object
    wasm_hook_transaction: bool
    contract_ibc_forward: bool

    def __init__(self, **kwargs):
        if "type" in kwargs:
            assert kwargs["type"] == RouteOperationType.SWAP.value
            del kwargs["type"]

        super().__init__(type=RouteOperationType.SWAP, **kwargs)
        self.price_impact = kwargs["priceImpact"]
        self.chain_name = kwargs["chainName"]
        self.chain_id = kwargs["chainId"]
        self.routes = kwargs["routes"]
        self.alternatives = kwargs["alternatives"]
        self.wasm_hook_transaction = kwargs["wasmHookTransaction"]
        self.contract_ibc_forward = kwargs["contractIbcForward"]


@dataclass
class RouteOperationTransfer(RouteOperation):
    source_denom: str
    destination_denom: str
    source_chain_id: str
    destination_chain_id: str
    source_chain_name: str
    destination_chain_name: str
    source_channel: str
    destination_channel: str
    source_port: str
    destination_port: str
    pfm_transaction: bool

    def __init__(self, **kwargs):
        super().__init__(type=RouteOperationType.TRANSFER, **kwargs)
        self.source_denom = kwargs["sourceDenom"]
        self.destination_denom = kwargs["destinationDenom"]
        self.source_chain_id = kwargs["sourceChainId"]
        self.destination_chain_id = kwargs["destinationChainId"]
        self.source_chain_name = kwargs["sourceChainName"]
        self.destination_chain_name = kwargs["destinationChainName"]
        self.source_channel = kwargs["sourceChannel"]
        self.destination_channel = kwargs["destinationChannel"]
        self.source_port = kwargs["sourcePort"]
        self.destination_port = kwargs["destinationPort"]
        self.pfm_transaction = kwargs["pfmTransaction"]


@dataclass(init=False)
class Route(UnderscoreOrCamelCaseMeta):
    input_amount: int
    return_amount: int
    source_chain_id: str
    destination_chain_id: str
    source_chain_name: str
    destination_chain_name: str
    ask_token: str
    offer_token: str
    routes: list[RouteOperation]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.routes = []
        for r in kwargs["routes"]:
            route_type = r.pop("type")
            match route_type:
                case RouteOperationType.SWAP.value:
                    self.routes.append(RouteOperationSwap(**r))
                case RouteOperationType.TRANSFER.value:
                    self.routes.append(RouteOperationTransfer(**r))
                case _:
                    raise Exception(f"Unknown route type: {route_type}")


@dataclass
class Swap:
    type: SwapType
    chain_id: str
    chain_name: str
    msg: list[object]

    def __init__(self, **kwargs):
        self.type = kwargs["type"]
        self.chain_id = kwargs["chainID"]
        self.chain_name = kwargs["chainName"]
        self.msg = kwargs["msg"]


class IbcTransferSwap(Swap):
    destination_chain_id: str
    destination_chain_name: str
    source_channel: str
    destination_channel: str
    source_port: str
    destination_port: str

    def __init__(self, **kwargs):
        super().__init__(
            type=SwapType.IBC_TRANSFER,
            chainID=kwargs["chainID"],
            chainName=kwargs["chainName"],
            msg=kwargs["msg"],
        )
        self.destination_chain_id = kwargs["destinationChainID"]
        self.destination_chain_name = kwargs["destinationChainName"]
        self.source_channel = kwargs["sourceChannel"]
        self.destination_channel = kwargs["destinationChannel"]
        self.source_port = kwargs["sourcePort"]
        self.destination_port = kwargs["destinationPort"]


@dataclass(init=False)
class RouteAndMsgs:
    route: RouteOperation
    msgs: list[Swap]

    def __init__(self, route, msgs):
        self.route = Route(**route)
        self.msgs = [
            IbcTransferSwap(**row) if row["type"] == SwapType.IBC_TRANSFER.value else Swap(**row) for row in msgs
        ]
