from unittest import mock

import pytest
from httpx import AsyncClient

from carnage.api.routes import authentication
from tests.unit_tests.conftest import APPLICATION_PREFIX

BASE_URL = f"http://test/{APPLICATION_PREFIX}/authentication"


@pytest.mark.anyio()
async def test_google_login(application_instance):
    with mock.patch.object(
        authentication.google.route.oauth.google,
        "authorize_access_token",
        mock.AsyncMock(),
    ):
        async with AsyncClient(
            app=application_instance,
            base_url=BASE_URL,
        ) as ac:
            response = await ac.get("/google/login")
        assert response.status_code == 302


@pytest.mark.anyio()
async def test_google_auth(application_instance):
    with (
        mock.patch.object(
            authentication.google.route.oauth.google,
            "authorize_access_token",
            mock.AsyncMock(return_value={"userinfo": {"email": "test"}}),
        ),
        mock.patch.object(
            authentication.google.route.account_repository,
            "select_by_username",
        ),
    ):
        async with AsyncClient(
            app=application_instance,
            base_url=BASE_URL,
        ) as ac:
            response = await ac.get("/google/auth")
        assert response.status_code == 200
        assert isinstance(response.text, str)


@pytest.mark.anyio()
async def test_google_auth_no_user_found(application_instance):
    with (
        mock.patch.object(
            authentication.google.route.oauth.google,
            "authorize_access_token",
            mock.AsyncMock(return_value={"userinfo": {"email": "test"}}),
        ),
        mock.patch.object(
            authentication.google.route.account_repository,
            "select_by_username",
            lambda username: False,
        ),
        mock.patch.object(
            authentication.google.route.account_repository,
            "insert",
            lambda data: None,
        ),
    ):
        async with AsyncClient(
            app=application_instance,
            base_url=BASE_URL,
        ) as ac:
            response = await ac.get("/google/auth")
        assert response.status_code == 200
        assert isinstance(response.text, str)
