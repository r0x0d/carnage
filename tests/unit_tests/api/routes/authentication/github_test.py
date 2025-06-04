from unittest import mock

import pytest
from httpx import AsyncClient

from carnage.api.routes import authentication
from tests.unit_tests.conftest import APPLICATION_PREFIX

BASE_URL = f"http://test/{APPLICATION_PREFIX}/authentication"


class HTTPXResponseMock:
    def __init__(self) -> None:
        pass

    def get(self, url, headers):
        return self

    def json(self):
        return {
            "id": "test",
            "email": "test",
            "name": "test",
            "login": "test",
            "html_url": "test",
            "avatar_url": "test",
            "blog": "test",
            "primary": True,
        }


class HTTPXMultipleResponseMock:
    def __init__(self, email="test", is_primary=True) -> None:
        self.call = 0
        self.email = email
        self.is_primary = is_primary

    def get(self, url, headers):
        return self

    def json(self):
        data = {
            "id": "test",
            "email": None,
            "name": "test",
            "login": "test",
            "html_url": "test",
            "avatar_url": "test",
            "blog": "test",
            "primary": False,
        }
        if self.call == 0:
            self.call += 1
            return data
        else:
            data["email"] = self.email
            data["primary"] = self.is_primary
            return [data]


@pytest.mark.anyio()
async def test_github_login(application_instance):
    with mock.patch.object(
        authentication.github.route.oauth.github,
        "authorize_access_token",
        mock.AsyncMock(),
    ):
        async with AsyncClient(
            app=application_instance,
            base_url=BASE_URL,
        ) as ac:
            response = await ac.get("/github/login")
        assert response.status_code == 302


@pytest.mark.anyio()
async def test_github_auth(application_instance):
    with (
        mock.patch.object(
            authentication.github.route.oauth.github,
            "authorize_access_token",
            mock.AsyncMock(return_value={"access_token": "test"}),
        ),
        mock.patch.object(
            authentication.github.route.account_repository,
            "select_by_username",
        ),
        mock.patch.object(
            authentication.github.httpx,
            "get",
            return_value=HTTPXResponseMock(),
        ),
    ):
        async with AsyncClient(
            app=application_instance,
            base_url=BASE_URL,
        ) as ac:
            response = await ac.get("/github/auth")
        assert response.status_code == 200
        assert isinstance(response.text, str)


@pytest.mark.anyio()
async def test_github_auth_no_user_found(application_instance):
    with (
        mock.patch.object(
            authentication.github.route.oauth.github,
            "authorize_access_token",
            mock.AsyncMock(return_value={"access_token": "test"}),
        ),
        mock.patch.object(
            authentication.github.route.account_repository,
            "select_by_username",
            lambda username: False,
        ),
        mock.patch.object(
            authentication.github.route.account_repository,
            "insert",
            lambda data: None,
        ),
        mock.patch.object(
            authentication.github.httpx,
            "get",
            return_value=HTTPXResponseMock(),
        ),
    ):
        async with AsyncClient(
            app=application_instance,
            base_url=BASE_URL,
        ) as ac:
            response = await ac.get("/github/auth")
        assert response.status_code == 200
        assert isinstance(response.text, str)


@pytest.mark.anyio()
async def test_github_auth_no_primary_email(application_instance):
    with (
        mock.patch.object(
            authentication.github.route.oauth.github,
            "authorize_access_token",
            mock.AsyncMock(return_value={"access_token": "test"}),
        ),
        mock.patch.object(
            authentication.github.route.account_repository,
            "select_by_username",
        ),
        mock.patch.object(
            authentication.github.httpx,
            "get",
            return_value=HTTPXMultipleResponseMock(),
        ),
    ):
        async with AsyncClient(
            app=application_instance,
            base_url=BASE_URL,
        ) as ac:
            response = await ac.get("/github/auth")
        assert response.status_code == 200
        assert isinstance(response.text, str)


@pytest.mark.anyio()
async def test_github_auth_no_primary_email_at_all(application_instance):
    with (
        mock.patch.object(
            authentication.github.route.oauth.github,
            "authorize_access_token",
            mock.AsyncMock(return_value={"access_token": "test"}),
        ),
        mock.patch.object(
            authentication.github.route.account_repository,
            "select_by_username",
        ),
        mock.patch.object(
            authentication.github.httpx,
            "get",
            return_value=HTTPXMultipleResponseMock(email="", is_primary=False),
        ),
    ):
        async with AsyncClient(
            app=application_instance,
            base_url=BASE_URL,
        ) as ac:
            response = await ac.get("/github/auth")
        assert response.status_code == 200
        assert isinstance(response.text, str)
