class SmsActivateError(Exception): ...
class NoBalance(SmsActivateError): ...
class NoNumbers(SmsActivateError): ...