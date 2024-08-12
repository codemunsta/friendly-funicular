from typing import Union

PHONE_NUMBER_MAX_LENGTH = 13
PHONE_NUMBER_MIN_LENGTH = 11
MIN_CHAR_FIELD_LENGTH = 25
MAX_CHAR_FIELD_LENGTH = 256
DEFAULT_USER_ACCOUNT_STATUS = "Active"
FRONTEND_URL = ""


def success_response(code: int, message: str, data):
    return {"status": "Success", "code": code, "message": str(message), "data": data}


class ResponseError:

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def __str__(self):
        return f"Error(code={self.code}, message='{self.message}')"

    def to_dict(self) -> dict:
        return {"code": self.code, "message": self.message}


def error_response(code: int, message: Union[str, Exception], error: ResponseError):
    return {"status": "Failed", "code": code, "message": str(message), "error": error.to_dict()}
