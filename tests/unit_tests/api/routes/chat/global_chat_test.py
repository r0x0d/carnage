from collections import namedtuple
from unittest import mock

from fastapi.testclient import TestClient

from carnage.api.routes.chat import global_chat

AccountModelOutput = namedtuple("AccountModelOutput", ("secret_key"))


def test_websocket(database_session_mock, application_instance, get_fake_jwt):
    # Random fernet key generated for testing purposes.
    output = AccountModelOutput("_UCCQZGUSHZMa5P5bmdYgo7T-k1p25o5Ejl_qMu1ONg=")
    client = TestClient(application_instance)
    with (
        mock.patch.object(
            global_chat.route.account_repository,
            "select_by_id",
            lambda identifier: [output],
        ),
        mock.patch.object(global_chat.route, "repository"),
    ):
        with client.websocket_connect(
            f"/api/v1/chat/global/9a22bdfa-6adb-11ed?token={get_fake_jwt}",
        ) as websocket:
            websocket.send_json(
                {
                    "message": "test",
                    "channel": "dd4dc11e-6adc-11ed-9ae1-641c67e34d72",
                },
                mode="text",
            )
