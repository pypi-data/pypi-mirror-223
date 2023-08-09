from .enums import NetworkType
from .utils import get_or, underscore_to_camelcase


class UnderscoreOrCamelCaseMeta:
    FORCE_TYPES = {
        "network_type": NetworkType,
    }

    def __init__(self, sdk=None, **kwargs):
        self.sdk = sdk

        for field_name, _ in self.__dataclass_fields__.items():
            var = get_or(kwargs, field_name, underscore_to_camelcase(field_name))
            if field_name in self.FORCE_TYPES:
                var = self.FORCE_TYPES[field_name](var)

            setattr(self, field_name, var)
