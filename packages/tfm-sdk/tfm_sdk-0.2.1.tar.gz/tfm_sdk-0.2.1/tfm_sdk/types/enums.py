import enum


class NetworkType(enum.Enum):
    MAINNET = "MAINNET"
    TESTNET = "TESTNET"

    def __str__(self):
        return self.value


class RouteOperationType(enum.Enum):
    SWAP = "chain_swap_operations"
    TRANSFER = "ibc_transfer"


class TokenType(enum.Enum):
    NATIVE = "native"
    IBC = "ibc"

    def __str__(self):
        return self.value


class SwapType(enum.Enum):
    IBC_TRANSFER = "ibc_transfer"
    SWAP = "swap"

    def __str__(self):
        return self.value


class SwapMode(enum.Enum):
    TURBO = "Turbo"
    SAVING = "Saving"

    def __str__(self):
        return self.value
