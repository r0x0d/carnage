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
            "public_email": "test",
            "email": "test",
            "name": "test",
            "username": "test",
            "web_url": "test",
            "avatar_url": "test",
            "website_url": "test",
        }


@pytest.mark.anyio()
async def test_gitlab_login(application_instance):
    with mock.patch.object(
        authentication.gitlab.route.oauth.gitlab,
        "authorize_access_token",
        mock.AsyncMock(),
    ):
        async with AsyncClient(
            app=application_instance,
            base_url=BASE_URL,
        ) as ac:
            response = await ac.get("/gitlab/login")
        assert response.status_code == 302


@pytest.mark.anyio()
async def test_gitlab_auth(application_instance):
    with (
        mock.patch.object(
            authentication.gitlab.route.oauth.gitlab,
            "authorize_access_token",
            mock.AsyncMock(return_value={"access_token": "test"}),
        ),
        mock.patch.object(
            authentication.gitlab.route.account_repository,
            "select_by_username",
        ),
        mock.patch.object(
            authentication.gitlab.httpx,
            "get",
            return_value=HTTPXResponseMock(),
        ),
    ):
        async with AsyncClient(
            app=application_instance,
            base_url=BASE_URL,
        ) as ac:
            response = await ac.get("/gitlab/auth")
        assert response.status_code == 200
        assert isinstance(response.text, str)


@pytest.mark.anyio()
async def test_gitlab_auth_no_user_found(application_instance):
    with (
        mock.patch.object(
            authentication.gitlab.route.oauth.gitlab,
            "authorize_access_token",
            mock.AsyncMock(return_value={"access_token": "test"}),
        ),
        mock.patch.object(
            authentication.gitlab.route.account_repository,
            "select_by_username",
            lambda username: False,
        ),
        mock.patch.object(
            authentication.gitlab.route.account_repository,
            "insert",
            lambda data: None,
        ),
        mock.patch.object(
            authentication.gitlab.httpx,
            "get",
            return_value=HTTPXResponseMock(),
        ),
    ):
        async with AsyncClient(
            app=application_instance,
            base_url=BASE_URL,
        ) as ac:
            response = await ac.get("/gitlab/auth")
        assert response.status_code == 200
        assert isinstance(response.text, str)
