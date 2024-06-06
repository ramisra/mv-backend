import json
from pathlib import Path
from typing import Optional

from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    SecurityScopes,
)
from fastapi_auth0.auth import JwksDict
from jose import ExpiredSignatureError, jwt

from core.config import get_settings
from core.crud.user import UserCrud
from core.database import get_db_session
from core.models.user import User
from core.utils.custom_exceptions import UnauthenticatedException, UnauthorizedException


class AuthService:
    """Does all the token verification using PyJWT"""

    def __init__(self):
        settings = get_settings()
        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        self.audience = settings.OAUTH_PROVIDER_CLIENT_ID
        self.algorithm = "RS256"
        self.issuer = (
            f'https://{settings.OAUTH_PROVIDER_CLIENT_DOMAIN}/'
        )
        jwt_validation_public_keys = (
                Path(__file__).resolve().parent.parent.parent / 'auth_jwks.json'
        )
        secrets_file = open(jwt_validation_public_keys, "r")
        self.jwks: JwksDict = json.load(secrets_file)

    @staticmethod
    def handle_exception(e: Exception):
        if isinstance(e, UnauthorizedException):
            raise e
        elif isinstance(e, ExpiredSignatureError):
            raise UnauthenticatedException("Token has expired")
        else:
            raise UnauthenticatedException("Invalid Token")

    async def verify_token(self, credentials: str) -> Optional[dict]:
        # This gets the 'kid' from the passed token
        # unverified_header = jwt.get_unverified_header(credentials)
        # #
        # if "kid" not in unverified_header:
        #     raise UnauthenticatedException(detail="Malformed token header")
        rsa_key = {}
        for key in self.jwks["keys"]:
            # if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                break
        if rsa_key:
            payload = jwt.decode(
                credentials,
                rsa_key['n']
            )

            db = next(get_db_session())
            if not UserCrud.get_user_from_email(db, payload["email"]):
                raise UnauthorizedException(detail="User not authorized")
            return payload
        else:
            msg = "Invalid kid header (wrong tenant or rotated public key)"
            raise UnauthenticatedException(detail=msg)

    def generate_token(self, claims) -> str:
        # This gets the 'kid' from the passed token
        rsa_key = {}
        for key in self.jwks["keys"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
            break
        if rsa_key:

            token = jwt.encode(
                claims,
                rsa_key['n']
            )
            return token
        else:
            msg = "Authentication Failed"
            raise UnauthenticatedException(detail=msg)

    async def get_current_user(
        self,
        security_scopes: SecurityScopes,
        token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    ) -> Optional[User]:
        if token is None:
            return None

        try:
            payload = await self.verify_token(token.credentials)
            db = next(get_db_session())
            user = UserCrud.get_user_from_email(db, payload["email"])
            return user
        except Exception as e:
            AuthService.handle_exception(e)

    async def is_user_logged_in(
        self,
        security_scopes: SecurityScopes,
        token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer()),
    ):
        if token is None:
            raise UnauthenticatedException("Malformed Auth")
        try:
            await self.verify_token(token.credentials)
        except Exception as e:
            raise UnauthenticatedException("Malformed Auth")

    async def verify_admin_access(
        self,
        security_scopes: SecurityScopes,
        token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer()),
    ):
        if token is None:
            raise UnauthenticatedException
        try:
            payload = await self.verify_token(token.credentials)
            db = next(get_db_session())
            user = UserCrud.get_user_from_email(db, payload["email"])
            if not user.is_admin:
                raise UnauthorizedException(
                    detail="User not authorized to perform this action"
                )
        except Exception as e:
            AuthService.handle_exception(e)

