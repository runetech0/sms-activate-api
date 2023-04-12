import aiohttp
import typing
from . import errors as errors
from .activation import Activation as Activation
from .country import Country as Country, ServiceCountry as ServiceCountry
from .enums import Action as Action, ErrorsText as ErrorsText
from .logger import logger as logger
from _typeshed import Incomplete
from typing import Any, Dict, List, Optional, Union

class SmsActivateClient:
    all_countries: List[Country]
    api_key: Incomplete
    api_url: Incomplete
    debug: Incomplete
    def __init__(self, api_key: str, enable_whitelist: bool = ..., countries_whitelist: List[int] = ..., debug: bool = ..., proxy: Optional[str] = ...) -> None: ...
    def escape(self, value: str) -> str: ...
    async def close(self) -> None: ...
    async def check_resp(self, resp: aiohttp.ClientResponse) -> None: ...
    async def get_countries_list(self) -> typing.List[Country]: ...
    async def get_country_by_country_code(self, code: str) -> Optional[Country]: ...
    async def get_balance(self) -> float: ...
    async def top_countries_by_service(self, service: str, exclude_zero_counts: int = ...) -> List[ServiceCountry]: ...
    async def buy_number_free_price(self, service: str, max_price: int, phone_exceptions: List[Optional[int]] = ...) -> Activation: ...
    async def buy_number_by_country(self, service: str, country_id: typing.Union[str, int]) -> Activation: ...
    async def update_activation_status(self, activation_id: str, status: int) -> Union[str, Dict[str, Any]]: ...
    async def get_activation_status(self, activation_id: str) -> Union[str, Dict[str, Any]]: ...
    async def get_country_codes_by_service(self, service: str) -> List[int]: ...
    async def buy_number_any_country(self, service: str, tries: int = ...) -> Activation: ...
