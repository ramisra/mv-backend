from fastapi import HTTPException, Request
from starlette.responses import JSONResponse


class UnauthenticatedException(HTTPException):
    def __init__(self, detail: str, **kwargs):
        """Returns HTTP 401"""
        self.detail = detail
        self.status_code=403


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str, **kwargs):
        """Returns HTTP 403"""
        self.detail = detail


class CustomException(Exception):
    def __init__(self, detail: str, **kwargs):
        """Returns HTTP 500"""


async def handle_unauthenticated_exception(request: Request, exc: UnauthenticatedException):
    return JSONResponse(
        status_code=403,
        content={"message": f"{exc.detail}"},
    )


async def handle_unauthorized_exception(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code=403,
        content={"message": f"{exc.detail}"},
    )


async def handle_custom_exception(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=500,
        content={"message": "Something went wrong!"}
    )
