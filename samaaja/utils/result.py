from dataclasses import dataclass
from typing import Any, Dict
from samaaja.api.common import custom_response

@dataclass
class Result:
    message: str
    data: Any = None
    is_bad_request: bool = False
    is_not_found: bool = False
    is_internal_server_error: bool = False
    error_data: Any = None

    @classmethod
    def new(cls) -> "Result":
        return cls(message="", data=None, is_bad_request=False, is_not_found=False, is_internal_server_error=False, error_data=None)
    
    @classmethod
    def success(cls, message: str, data: Any = None) -> "Result":
        return cls(message=message, data=data, is_bad_request=False, is_not_found=False, is_internal_server_error=False)

    @classmethod
    def failure(cls, message: str, data: Any = None, error_data: Any = None) -> "Result":
        return cls(message=message, data=data, is_bad_request=False, is_not_found=False, is_internal_server_error=True, error_data=error_data)


    @classmethod
    def not_found(cls, message: str, data: Any = None) -> "Result":
        return cls(message=message, data=data, is_bad_request=False, is_not_found=True, is_internal_server_error=False)

    @classmethod
    def bad_request(cls, message: str, data: Any = None) -> "Result":
        return cls(message=message, data=data, is_bad_request=True, is_not_found=False, is_internal_server_error=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message": self.message,
            "data": self.data,
            "is_bad_request": self.is_bad_request,
            "is_not_found": self.is_not_found,
            "is_internal_server_error": self.is_internal_server_error,
            "error_data": self.error_data,
        }

    def to_custom_response(self) -> custom_response:
        if self.is_bad_request:
            return custom_response(message=self.message, data=self.data, status_code=400)
        elif self.is_not_found:
            return custom_response(message=self.message, data=self.data, status_code=404)
        elif self.is_internal_server_error:
            return custom_response(message=self.message, data=self.data, status_code=500)
        else:
            return custom_response(message=self.message, data=self.data, status_code=200)