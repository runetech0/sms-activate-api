from typing import *
from .client import SmsActivateClient as SmsActivateClient
from _typeshed import Incomplete

class Country:
    client: Incomplete
    data: Incomplete
    id: Incomplete
    code: Incomplete
    chinese_name: Incomplete
    english_name: Incomplete
    multi_service: Incomplete
    rent: Incomplete
    retry: Incomplete
    visible: Incomplete
    russsian_name: Incomplete
    def __init__(self, client: SmsActivateClient, data: dict) -> None: ...
    def json(self): ...

class ServiceCountry:
    client: Incomplete
    country_id: Incomplete
    numbers_count: Incomplete
    price: Incomplete
    retail_price: Incomplete
    def __init__(self, client: SmsActivateClient, data: dict) -> None: ...
