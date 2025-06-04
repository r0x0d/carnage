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
"""Module that implements the GitLab Route."""

import random
import string

import httpx
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from carnage.api.auth.authentication import generate_jwt
from carnage.api.routes.authentication.base import BaseAuthentication
from carnage.database.models.account import ProviderEnum


class GitlabAuthenticationRoute(BaseAuthentication):
    """Class that overrides the base routes for an API request."""

    def __init__(
        self,
        name: str = "gitlab",
    ) -> None:
        """Constructor for HTTP API route.

        :param name: The name of the route
        """
        super().__init__(
            name=name,
            config={
                "api_base_url": "https://gitlab.com/api/v4/",
                "authorize_url": "https://gitlab.com/oauth/authorize",
                "access_token_url": "https://gitlab.com/oauth/token",
                "client_kwargs": {"scope": "read_user"},
            },
        )

        self.router = APIRouter(
            prefix="/authentication",
            tags=["authentication"],
        )

        self.router.add_api_route(
            "/gitlab/login",
            self.gitlab_login,
            methods=["GET"],
            status_code=200,
        )
        self.router.add_api_route(
            "/gitlab/auth",
            self.gitlab_auth,
            methods=["GET"],
            status_code=200,
        )

    async def gitlab_login(self, request: Request) -> RedirectResponse:
        """Async method that handle the initial gitlab login page.

        :param request: The data send throught the request.
        """
        redirect_uri = request.url_for("gitlab_auth")
        return await self.oauth.gitlab.authorize_redirect(
            request,
            redirect_uri,
        )

    async def gitlab_auth(self, request: Request) -> str:
        """Async method that handles the authentication for gitlab.

        :param request: The data send throught the request.
        """
        token = await self.oauth.gitlab.authorize_access_token(request)

        userinfo = httpx.get(
            url="https://gitlab.com/api/v4/user",
            headers={
                "Authorization": f"Bearer {token['access_token']}",
            },
        ).json()

        claims = {
            "iss": "https://gitlab.com/api/v4",
            "azp": "gitlab.com",
            "sub": str(userinfo.get("id")),
            "email": userinfo.get("public_email")
            if userinfo.get("public_email")
            else userinfo.get("email"),
            "email_verified": True,  # TODO(r0x0d): Check later if gitlab returns this information # noqa
            "nonce": "".join(random.choice(string.ascii_letters) for _ in range(10)),
            "name": userinfo.get("name"),
            "preferred_username": userinfo.get("username"),
            "profile": userinfo.get("web_url"),
            "picture": userinfo.get("avatar_url"),
            "website": userinfo.get("website_url"),
        }

        await self.handle_user_account(
            username=claims["email"],
            nickname=claims["preferred_username"],
            provider=ProviderEnum.gitlab,
        )

        return generate_jwt(claims)


route = GitlabAuthenticationRoute()
