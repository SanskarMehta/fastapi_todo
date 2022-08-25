from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from todo_project import constants
from http import HTTPStatus
from config import Settings
from typing import Optional
import jwt
from datetime import timedelta


class JWTAuthentication:
    """
    fastapi-jwt-auth documentation link.
    https://indominusbyte.github.io/fastapi-jwt-auth/
    """

    # Use create_access_token() and create_refresh_token() to create our
    # access and refresh tokens

    def __init__(self, sub: str, authorize: AuthJWT = Depends(),
                 expires: Optional[timedelta] = Settings().JWT_TOKEN_EXPIRES,
                 ):
        self.expires = expires
        self.algorithm = Settings().JWT_ALGORITHM
        self.subject = sub
        self.Authorize = authorize

    def create_access_token(self):
        """
        This method is used to create the access token.
        :return: access token
        """
        return self.Authorize.create_access_token(subject=self.subject, expires_time=self.expires,
                                                  algorithm=self.algorithm, )

    def create_refresh_token(self):
        """
        This method is used to create the refresh token.
        :return: refresh token
        """
        return self.Authorize.create_refresh_token(subject=self.subject, expires_time=self.expires)

    def get_tokens_for_user(self):
        """
        This method is used to create the access and refresh token.
        :return: tokens
        """
        return {"access_token": self.create_access_token(), "refresh_token": self.create_refresh_token()}


class DecodeToken:
    def __init__(self, token: str, algorithm: Optional[str] = 'HS384'):
        self.token = token
        self.secret_key = Settings().authjwt_secret_key
        self.algorithm = algorithm

    def _decode(self):
        return jwt.decode(self.token, self.secret_key, self.algorithm)

    def decode_token(self):
        try:
            payload = self._decode()
            if payload['type'] == 'access':
                return payload['sub']
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=constants.MSG_SCOPE_INVALID_TOKEN)
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=constants.MSG_TOKEN_EXPIRE) from e
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=constants.MSG_TOKEN_INVALID) from e
