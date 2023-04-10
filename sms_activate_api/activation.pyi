import typing
from .client import SmsActivateClient as SmsActivateClient
from .country import Country as Country
from .errors import SmsActivateError as SmsActivateError
from .logger import logger as logger
from _typeshed import Incomplete
from typing import Optional

class ExpectedActivationStatus:
    STATUS_WAIT_CODE: str
    STATUS_WAIT_RETRY: str
    STATUS_WAIT_RESEND: str
    STATUS_CANCEL: str
    STATUS_OK: str

class ActivationStatus:
    SMS_SENT: int
    REQUEST_ANOTHER_CODE: int
    ACTIVATION_COMPLETE: int
    CANCEL_ACTIVATION: int

class Activation:
    client: Incomplete
    data: Incomplete
    activation_cost: Incomplete
    activation_id: Incomplete
    activation_operator: Incomplete
    activation_time: Incomplete
    can_get_another_sms: Incomplete
    country_code: Incomplete
    phone_number: Incomplete
    def __init__(self, client: SmsActivateClient, data: typing.Dict) -> None: ...
    def pprint(self) -> None: ...
    async def get_country_info(self) -> Optional[Country]: ...
    async def sms_sent(self): ...
    async def cancel_activation(self): ...
    async def request_another_sms(self): ...
    async def complete_activation(self): ...
    async def wait_for_code(self, timeout: int = ...) -> str: ...
