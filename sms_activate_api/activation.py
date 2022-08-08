
from __future__ import annotations
from typing import *
import asyncio
from .logger import logger
from .country import Country
from pprint import pprint


if TYPE_CHECKING:
    from .client import SmsActivateClient


class ExpectedActivationStatus:
    STATUS_WAIT_CODE = "STATUS_WAIT_CODE"
    STATUS_WAIT_RETRY = "STATUS_WAIT_RETRY"
    STATUS_WAIT_RESEND = "STATUS_WAIT_RESEND"
    STATUS_CANCEL = "STATUS_CANCEL"
    STATUS_OK = "STATUS_OK"


class ActivationStatus:
    SMS_SENT = 1
    REQUEST_ANOTHER_CODE = 3
    ACTIVATION_COMPLETE = 6
    CANCEL_ACTIVATION = 8


class Activation:
    def __init__(self, client: SmsActivateClient, data: Dict) -> None:
        self.client = client
        self.data = data
        self.activation_cost = data.get("activationCost")
        self.activation_id = data.get("activationId")
        self.activation_operator = data.get("activationOperator")
        self.activation_time = data.get("activationTime")
        self.can_get_another_sms = data.get("canGetAnotherSms")
        self.country_code = data.get("countryCode")
        self.phone_number = data.get("phoneNumber")

    def pprint(self):
        pprint(self.data)

    async def get_country_info(self) -> Country:
        return await self.client.get_country_by_country_code(self.country_code)

    async def sms_sent(self):
        return await self.client.update_activation_status(self.activation_id, ActivationStatus.SMS_SENT)

    async def cancel_activation(self):
        return await self.client.update_activation_status(self.activation_id, ActivationStatus.CANCEL_ACTIVATION)

    async def request_another_sms(self):
        return await self.client.update_activation_status(self.activation_id, ActivationStatus.REQUEST_ANOTHER_CODE)

    async def complete_activation(self):
        return await self.client.update_activation_status(self.activation_id, ActivationStatus.ACTIVATION_COMPLETE)

    async def wait_for_code(self, timeout=120) -> str:
        check_delay = 1
        current_time = 0
        while True:
            if current_time >= timeout:
                raise asyncio.TimeoutError("Timeout waiting for the code")
            status = await self.client.get_activation_status(self.activation_id)
            if ExpectedActivationStatus.STATUS_WAIT_CODE in status:
                await asyncio.sleep(check_delay)
                current_time += check_delay
                continue
            if ExpectedActivationStatus.STATUS_OK in status:
                return status.split(":")[-1]
            logger.debug(status)
            return status
