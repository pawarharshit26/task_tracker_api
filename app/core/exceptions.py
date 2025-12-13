class BaseException(Exception):
    message = "An error occured"

    def __init__(self, message: str | None = None):
        if message:
            self.message = message
