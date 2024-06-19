class TelegramException(Exception):
    def __init__(self, detail):
        self.detail = detail


class TokenInvalid(TelegramException):
    pass
