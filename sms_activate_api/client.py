import aiohttp

from . import errors
from urllib import parse
from .enums import Action, ErrorsText
from .activation import Activation
import json
from .country import Country, ServiceCountry
import typing
# from pprint import pprint
from .logger import logger
import logging
import random


class SmsActivateClient:

    all_countries = []

    def __init__(self, api_key,
                 enable_whitelist=False,
                 countries_whitelist: typing.List[int] = [],
                 debug=False,
                 proxy=None) -> None:
        if not debug:
            logger.setLevel(logging.ERROR)
        self.api_key = api_key
        self._enable_whitelist = enable_whitelist
        self._countries_whitelist = countries_whitelist
        self._proxy = proxy
        self._base = "https://api.sms-activate.org"
        self.api_url = f"{self._base}/stubs/handler_api.php"
        self._session = None
        self.debug = debug

    def escape(self, value: str):
        return parse.quote(str(value).encode("UTF-8"))

    def _param_dict_parse(self, params: dict):
        parsed = f"api_key={self.api_key}&json=1"
        # parsed = f"api_key={self.api_key}"
        if self.debug:
            parsed = f"{parsed}"
        for k, v in params.items():
            if parsed != "":
                parsed = f"{parsed}&{k}={self.escape(v)}"
            else:
                parsed = f"{k}={self.escape(v)}"
        return parsed

    async def close(self):
        if self._session is not None:

            return await self._session.close()

    async def check_resp(self, resp):
        text = await resp.text()
        if text == ErrorsText.NO_BALANCE:
            raise errors.NoBalance(text)
        if text == ErrorsText.NO_NUMBERS:
            raise errors.NoNumbers

    async def _request(self, params: dict, method: str = "GET", return_txt=False):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        url = f"{self.api_url}?{self._param_dict_parse(params)}"
        async with self._session.request(method=method, url=url, proxy=self._proxy) as r:
            await r.read()
        logger.debug(f"{method}:{url} returned [{r.status}]{r.reason}")
        await self.check_resp(r)
        if r.status == 200:
            if return_txt:
                return await r.text()
            return json.loads(await r.text())

    async def get_countries_list(self) -> typing.List[Country]:
        if len(self.all_countries) == 0:
            params = {
                "action": Action.GET_COUNTRIES_LIST
            }
            countries = await self._request(params, "GET")
            self.all_countries = [Country(self, data)
                                  for data in countries.values()]
        return self.all_countries

    async def get_country_by_country_code(self, code: str) -> Country:
        if len(self.all_countries) == 0:
            await self.get_countries_list()
        for country in self.all_countries:
            if str(code) == str(country.code):
                return country

    async def get_balance(self):
        params = {
            "action": Action.GET_BALANCE
        }
        r = await self._request(params, return_txt=True)
        return float(r.split(":")[-1])

    async def top_countries_by_service(self, service: str, exclude_zero_counts=True):
        params = {
            "action": Action.TOP_COUNTRIES_BY_SERVICE,
            "service": service,
            "freePrice": True
        }
        r = await self._request(params=params)
        service_countries = [ServiceCountry(self, d) for d in r]
        if exclude_zero_counts:
            return [country for country in service_countries if country.numbers_count > 0]

        return service_countries

    async def buy_number_free_price(self,
                                    service: str,
                                    max_price: int,
                                    phone_exceptions=[]
                                    ) -> Activation:
        params = {
            "action": Action.GET_NUMBER_V2,
            "service": service,
            "freePrice": True,
            "maxPrice": max_price,
        }
        exception_prefixes = ",".join([str(prefix)
                                      for prefix in phone_exceptions])
        if exception_prefixes != "":
            phone_exceptions = f"({exception_prefixes})"
        params.update({
            "phoneException": exception_prefixes
        })
        r = await self._request(params)
        return Activation(self, r)

    async def buy_number_by_country(self, service: str, country_id: typing.Union[str, int]) -> Activation:
        params = {
            "action": Action.GET_NUMBER_V2,
            "service": service,
            "freePrice": False,
            "country": country_id
        }
        r = await self._request(params)
        return Activation(self, r)

    async def update_activation_status(self, activation_id: str, status: int):
        params = {
            "action": Action.SET_STATUS,
            "status": status,
            "id": activation_id
        }
        return await self._request(params, return_txt=True)

    async def get_activation_status(self, activation_id: str):
        params = {
            "action": Action.GET_STATUS,
            "id": activation_id
        }
        return await self._request(params, return_txt=True)

    async def get_country_codes_by_service(self, service: str):
        params = {
            "action": "getTopCountriesByService",
            "service": service,
        }
        r = await self._request(params)
        codes = []
        for c in r:
            if self._enable_whitelist:
                cnt = c["country"]
                if cnt not in self._countries_whitelist:
                    continue

            if c["count"] == 0:
                continue
            codes.append(c["country"])

        return codes

    async def buy_number_any_country(self, service: str, tries=20):
        codes = await self.get_country_codes_by_service(service)
        assert len(codes) > 0
        for _ in range(tries):
            try:
                country_code = random.choice(codes)
                return await self.buy_number_by_country(service, country_code)
            except errors.NoNumbers:
                continue
