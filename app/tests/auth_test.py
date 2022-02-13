import json
from uuid import uuid4

import pytest
import requests

from app.database.schemas.users_schemas import User

# this is needed for the authorization fixture, don't delete!
from app.tests.config import base_url

user_data = {"username": f"kamron{uuid4()}", "password": "kamron"}


@pytest.mark.parametrize("data, status", [
    (user_data, 200),
    (user_data, 400),  # duplicate
    ({"usernames": 12, "pasword": "kamron"}, 422),  # invalid data
])
def test_sign_up(data, status):
    headers = {'content-type': 'application/json'}
    response = requests.post(f"{base_url}/auth/sign-up/", data=json.dumps(data), headers=headers)
    assert response.status_code == status
    if status == 200:
        assert response.json()["access_token"]
        assert response.json()["token_type"] == "bearer"


@pytest.mark.parametrize("data, status", [
    (user_data, 200),
    ({"username": "kamron4646", "password": "ka@mron"}, 401),  # invalid user
    ({"usernames": 12, "pasword": "kamron"}, 422),  # invalid data
])
def test_sign_in(data, status):
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(f"{base_url}/auth/sign-in/", data=data, headers=headers)
    assert response.status_code == status
    if status == 200:
        assert response.json()["access_token"]
        assert response.json()["token_type"] == "bearer"
        return response.json()["access_token"]


@pytest.mark.parametrize("user_token, status", [
    ("", 200),
    ("asdkl;asd.askdl;asd.asd", 401),  # invalid token
    (234, 401),  # invalid data
])
def test_get_user(token, user_token, status):
    if status == 200:
        user_token = token
    headers = {'content-type': 'application/json', 'Authorization': f'Bearer {user_token}'}
    response = requests.get(f"{base_url}/auth/get_user/", headers=headers)
    assert response.status_code == status
    if status == 200:
        assert User.parse_obj(response.json())


@pytest.mark.parametrize("data, status", [
    ({"username": f"kamron4646{uuid4()}", "password": "ka@mron"}, 200),
    ({"usernames": 12, "pasword": "kamron"}, 422),  # invalid data
])
def test_update_user(token, data, status):
    headers = {'content-type': 'application/json', 'Authorization': f'Bearer {token}'}
    response = requests.put(f"{base_url}/auth/update_user/", data=json.dumps(data), headers=headers)
    assert response.status_code == status
    if status == 200:
        assert response.json()["access_token"]
        assert response.json()["token_type"] == "bearer"


@pytest.mark.parametrize("user_token, status", [
    ("", 204),
    ("asdkl;asd.askdl;asd.asd", 401),  # invalid token
    (234, 401),  # invalid data
])
def test_delete_user(token, user_token, status):
    if status == 204:
        user_token = token
    headers = {'content-type': 'application/json', 'Authorization': f'Bearer {user_token}'}
    response = requests.delete(f"{base_url}/auth/delete_user/", headers=headers)
    assert response.status_code == status
