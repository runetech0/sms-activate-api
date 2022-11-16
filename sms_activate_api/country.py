from __future__ import annotations
from typing import *

if TYPE_CHECKING:
    from .client import SmsActivateClient


class Country:
    def __init__(self, client: SmsActivateClient, data: dict) -> None:
        self.client = client
        self.data = data
        self.id = data.get("id")
        self.code = self.id
        self.chinese_name = data.get("chn", None)
        self.english_name = data.get("eng")
        self.multi_service = bool(data.get("multiService", False))
        self.rent = bool(data.get("rent"))
        self.retry = bool(data.get("retry"))
        self.visible = bool(data.get("visible"))
        self.russsian_name = bool(data.get("rus"))

    def __repr__(self) -> str:
        return f"{self.id}: {self.english_name}"

    def __str__(self) -> str:
        return f"{self.id}: {self.english_name}"

    def json(self):
        return self.data


class ServiceCountry:
    def __init__(self, client: SmsActivateClient, data: dict) -> None:
        self.client = client
        self.country_id = data.get("country")
        self.numbers_count = data.get("count")
        self.price = data.get("price")
        self.retail_price = data.get("retail_price")

    def __repr__(self) -> str:
        return f"{self.country_id}: {self.price}/{self.retail_price}"

    def __str__(self) -> str:
        return f"{self.country_id}: {self.price}/{self.retail_price}"
