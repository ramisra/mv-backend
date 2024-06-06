from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from starlette.middleware.sessions import SessionMiddleware

from core.api.v1.routes import MAIN_ROUTER
from core.config import Settings, TestSettings
from core.utils.custom_exceptions import (
    CustomException,
    UnauthenticatedException,
    UnauthorizedException,
    handle_custom_exception,
    handle_unauthenticated_exception,
    handle_unauthorized_exception,
)


def create_app(settings: Union[Settings, TestSettings]):

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/docs",
        description=settings.DESCRIPTION,
        debug=settings.DEBUG,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://frontend:8080/",
            "http://frontend:8080/",
            "*",
        ],
        # origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    app.include_router(MAIN_ROUTER)
    app.add_middleware(SessionMiddleware, secret_key="abc")
    # Instrumentator().instrument(app).expose(app)
    app.add_exception_handler(
        UnauthenticatedException, handle_unauthenticated_exception
    )
    app.add_exception_handler(
        UnauthorizedException, handle_unauthorized_exception
    )
    app.add_exception_handler(CustomException, handle_custom_exception)
    add_pagination(app)
    return app
