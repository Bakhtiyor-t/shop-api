import json
import sys
from uuid import uuid4

import pytest
import requests
from _pytest.fixtures import SubRequest

from app.database.schemas.users_schemas import User
from app.tests.config import base_url

sys.dont_write_bytecode = True


def _get_user_id(token):
    headers = {'content-type': 'application/json', 'Authorization': f'Bearer {token}'}
    response = requests.get(f"{base_url}/auth/get_user/", headers=headers)
    assert response.status_code == 200
    assert User.parse_obj(response.json())
    return response.json()["id"]


def _create_user(data=None):
    if data is None:
        data = {"username": f"baxti{uuid4()}", "password": "baxti01"}
    headers = {'content-type': 'application/json'}
    response = requests.post(f"{base_url}/auth/sign-up/", data=json.dumps(data), headers=headers)
    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"
    return response.json()["access_token"]


def _delete_user(token):
    headers = {'content-type': 'application/json', 'Authorization': f'Bearer {token}'}
    response = requests.delete(f"{base_url}/auth/delete_user/", headers=headers)
    assert response.status_code == 204


def _token(data):
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(f"{base_url}/auth/sign-in/", data=data, headers=headers)
    return response.json()["access_token"]


@pytest.fixture(scope="module")
def token(request: SubRequest):
    data = getattr(request.module, "user_data")
    return _token(data)


@pytest.fixture(scope="module")
def get_user():
    token = _create_user()
    yield token
    _delete_user(token)


@pytest.fixture(scope="module")
def five_new_users():
    users = []
    for _ in range(5):
        token = _create_user({"username": f"timur{uuid4()}", "password": "timur"})
        user_id = _get_user_id(token)
        users.append({"id": user_id, "token": token})
    yield users
    for user in users:
        _delete_user(user["token"])


@pytest.fixture
def get_user_id():
    return _get_user_id
