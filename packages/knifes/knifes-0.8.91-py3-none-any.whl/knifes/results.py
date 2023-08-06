from __future__ import annotations
from django.http import JsonResponse
from django.utils.translation import gettext as _
from .jsons import ObjectEncoder
from typing import Optional
from enum import Enum


class BaseErrorEnum(Enum):
    """
    error code is negative number
    """
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg

    @classmethod
    def get_by_code(cls, code) -> Optional[BaseErrorEnum]:
        return next(filter(lambda x: x.code == code, cls.__members__.values()), None)


class ApiResponse:
    def __init__(self, code, *, msg=None, data=None):
        self.code = code
        self.succ = (code == 200)
        self.msg = msg
        self.data = data

    # @classmethod
    # def fail(cls, msg, code=400, msg_detail=None):
    #     return ApiResult(code, msg=msg, msg_detail=msg_detail)
    #
    # @classmethod
    # def succ(cls, data=None):
    #     return ApiResult(200, data=data)

    @classmethod
    def success(cls, data=None):
        return JsonResponse(ApiResponse(200, data=data), encoder=ObjectEncoder, safe=False)

    @classmethod
    def failure(cls, msg, code=400):
        return JsonResponse(ApiResponse(code, msg=msg), encoder=ObjectEncoder, safe=False)

    @classmethod
    def error(cls, error_enum: BaseErrorEnum):
        return JsonResponse(ApiResponse(error_enum.code, msg=error_enum.msg), encoder=ObjectEncoder, safe=False)

    @classmethod
    def missing_param(cls, msg=_('缺少参数')):
        return cls.failure(msg)

    @classmethod
    def unauthorized(cls, msg=_('请先登录')):
        return cls.failure(msg, code=401)

    # @classmethod
    # def tokenInvalid(cls, msg=_('请先登录')):
    #     return cls.failResponse(msg, code=300)


class InternalApiResponse(ApiResponse):
    def __init__(self, code, *, msg=None, data=None, msg_detail=None):
        super().__init__(code, msg=msg, data=data)
        self.msg_detail = msg_detail

    @classmethod
    def error(cls, error_enum: BaseErrorEnum, msg_detail=None):
        return JsonResponse(InternalApiResponse(error_enum.code, msg=error_enum.msg, msg_detail=msg_detail), encoder=ObjectEncoder, safe=False)

