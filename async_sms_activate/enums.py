

class Action:
    GET_COUNTRIES_LIST = "getCountries"
    TOP_COUNTRIES_BY_SERVICE = "getTopCountriesByService"
    GET_BALANCE = "getBalance"
    GET_NUMBER = "getNumber"
    GET_NUMBER_V2 = "getNumberV2"  # Same as getNumber but returns some additonal info
    SET_STATUS = "setStatus"
    GET_STATUS = "getStatus"


class Service:
    # See full list of services at: https://sms-activate.org/en/api2#topCountries
    FULL_RENT = "full"
    TELEGRAM = "tg"
    DISCORD = "ds"
    TWITTER = "tw"
    INSTAGRAM = "ig"


class ErrorsText:
    NO_BALANCE = "NO_BALANCE"
    NO_NUMBERS = "NO_NUMBERS"
