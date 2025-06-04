# MIT License
#
# Copyright (c) 2022, Rodolfo Olivieri
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Module to handle the authentication process, as well, generating tokens."""

from datetime import datetime, timedelta
from typing import Any

from fastapi import HTTPException, Query, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.exceptions import ExpiredSignatureError

from carnage.constants import JWT_ALGORITHM, JWT_SECRET_KEY


def generate_jwt(claims: dict[str, Any]) -> str:
    """Generate a valid jwt token based on the claims provided.

    :param claims: Dictionary with claims from login providers.
    """
    if "aud" in claims:
        claims.pop("aud")

    if "at_hash" in claims:
        claims.pop("at_hash")

    # Replace or append whatever iat/exp that the claims have
    iat = datetime.utcnow()
    exp = iat + timedelta(hours=1)
    claims["iat"] = int(iat.timestamp())
    claims["exp"] = int(exp.timestamp())

    return jwt.encode(
        claims=claims,
        key=JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


class BaseJWTBearer(HTTPBearer):
    """Base class that implements the basic methods for JWT authentication."""

    def __init__(self, auto_error: bool = True):
        """Base class that handles the JWT Bearer authentication workflow.

        :param auto_error: If the class should error in case of any mismatch.
        """
        super().__init__(auto_error=auto_error)

    def verify_jwt(self, token: str) -> bool:
        """Verify if the JWT token passed on the request is valid or not.

        :param token: The token to be analyzed.
        """
        try:
            decoded_token = jwt.decode(
                token=token,
                key=JWT_SECRET_KEY,
                algorithms=[JWT_ALGORITHM],
            )
            utcnow = int(datetime.utcnow().timestamp())
            is_token_valid = decoded_token["exp"] >= utcnow
            return is_token_valid
        except ExpiredSignatureError:
            return False


class APIJWTBearer(BaseJWTBearer):
    """Class that handles the JWT authentication via Restful API request."""

    def __init__(self, auto_error: bool = True):
        """API class to handle JWT Bearer authentication throught requests.

        :param auto_error: If the class should error in case of any mismatch.
        """
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> bool:
        """Asynchronous handler for JWT Token verification.

        :param request: The request that contains the token.
        :raises HTTPException: In case of the token not being valid or the
            request is wrong.
        """
        credentials: HTTPAuthorizationCredentials = await super().__call__(
            request,
        )
        if credentials:
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403,
                    detail="Invalid token or expired token.",
                )
            return True

        raise HTTPException(
            status_code=403,
            detail="Invalid authorization code.",
        )


class WebSocketJWTBearer(BaseJWTBearer):
    """Class that handles the the JWT authentication via websockets."""

    def __init__(self, auto_error: bool = True):
        """Websocket class to handle JWT authentication throught requests.

        :param auto_error: If the class should error in case of any mismatch.
        """
        super().__init__(auto_error=auto_error)

    async def __call__(
        self,
        token: str | None = Query(default=None),
    ) -> bool:
        """Asynchronous handler for JWT Token verification.

        :param token: The token itself to be analyzed.
        :raises HTTPException: In case of the token not being valid or the
            request is wrong.
        """
        if token:
            if not self.verify_jwt(token):
                raise HTTPException(
                    status_code=403,
                    detail="Invalid token or expired token.",
                )
            return True

        raise HTTPException(
            status_code=403,
            detail="No token was provided.",
        )
