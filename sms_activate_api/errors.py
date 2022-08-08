

class SmsActivateError(Exception):
    """A General/base error"""


class NoBalance(SmsActivateError):
    """Out of balance"""


class NoNumbers(SmsActivateError):
    """No numbers available for country/service"""
