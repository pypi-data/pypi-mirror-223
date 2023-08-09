from ..api import TfmApi
from ..types import Chain


class SdkMixin:
    def __init__(self, sdk_instance):
        from tfm_sdk import TfmSdk

        self.sdk: TfmSdk = sdk_instance

    @property
    def api(self) -> TfmApi:
        return self.sdk.api

    @property
    def chains(self) -> list[Chain]:
        return self.sdk.get_chains()

    @property
    def source_chain(self) -> Chain:
        return self.sdk.source_chain

    @property
    def destination_chain(self) -> Chain:
        return self.sdk.destination_chain
