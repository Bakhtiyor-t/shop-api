import json
from uuid import uuid4

import pytest
import requests

from app.database.schemas.company_schemas import Company
from app.tests.basic_operations import BasicOperations
from app.tests.config import base_url, admin_user

# this is needed for the authorization fixture, don't delete!
user_data = admin_user
admin_user_id = 1
admin_company_name = "Tong"

basicOperations = BasicOperations()


@pytest.mark.parametrize("status", [
    200, 400
])
def test_get_company(token, get_user, status):
    basicOperations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="company/",
        schema=Company
    )
    basicOperations.get_items()


# Operations with create data
@pytest.mark.parametrize("data, status", [
    ({"name": f"Tong{uuid4()}"}, 200),  # new company name with net user
    ({"name": f"Tong{uuid4()}"}, 400),  # if user already in campaign
    ({"namesss": "Tong"}, 422),  # invalid data
])
def test_create_company(token, get_user, data, status):
    basicOperations.set_values(
        token=get_user,
        second_token=token,
        status=status,
        url=base_url,
        path="company/",
        schema=Company
    )
    basicOperations.create_items(data=json.dumps(data))


# Operations with update data
@pytest.mark.parametrize("data, status", [
    ({"name": f"Tong{uuid4()}"}, 200),  # new company name
    ({"name": admin_company_name}, 400),  # for duplicate company name
    # ({"name": f"Tong{uuid4()}"}, 400),  # user don't have company
    ({"namess": "Tong"}, 422)  # invalid data
])
def test_update_company(get_user, data, status):
    basicOperations.set_values(
        token=get_user,
        second_token=get_user,
        status=status,
        url=base_url,
        path="company/",
        schema=Company
    )
    basicOperations.update_items(data=json.dumps(data))


# here we take user indexes
# from five_new_users there are 5 new users
# Operations with adding a new user to the company.

# here we add all users to the company
@pytest.mark.parametrize("user_id, status", [
    (0, 200),  # from five_new_users
    (1, 200),  # from five_new_users
    (2, 200),  # from five_new_users
    (3, 200),  # from five_new_users
    (4, 200),  # from five_new_users
    (2555, 400),  # user don't have company
    ("name", 422)  # invalid data
])
def test_add_new_user(token, user_id, status, five_new_users):
    headers = {'content-type': 'application/json', 'Authorization': f'Bearer {token}'}
    if status == 200:
        user_id = five_new_users[user_id]["id"]
    response = requests.post(f"{base_url}/company/add_user/{user_id}/", headers=headers)
    assert response.status_code == status


# here we take user indexes
# from five_new_users there are 5 new users.

# here we remove one user from the company
# in this case the first one from the list five_new_users
@pytest.mark.parametrize("user_id, status", [
    (0, 204),  # from five_new_users
    (admin_user_id, 403),  # the user removes himself from the company
    ("namess", 422)  # invalid data
])
def test_delete_user(token, user_id, status, five_new_users, get_user_id):
    headers = {'content-type': 'application/json', 'Authorization': f'Bearer {token}'}
    if status == 204:
        user_id = five_new_users[user_id]["id"]
    if status == 403:
        user_id = get_user_id(token)
    response = requests.delete(f"{base_url}/company/delete_user/{user_id}/", headers=headers)
    assert response.status_code == status


# here we take user indexes
# from five_new_users there are 5 new users

# here we delete all users from the company
# except the first and last
@pytest.mark.parametrize("users_ids, status", [
    ("", 204),
    ([1], 403),  # from five_new_users, the user is not in the company
    ([123456, 983475], 400),  # invalid users id
    ("3", 422),  # invalid data
])
def test_delete_users(token, users_ids, status, five_new_users):
    headers = {'content-type': 'application/json', 'Authorization': f'Bearer {token}'}
    if status == 204:
        users_ids = [user["id"] for user in five_new_users[1:-1]]
    response = requests.delete(
        f"{base_url}/company/delete_users/",
        headers=headers,
        data=json.dumps(users_ids)
    )
    assert response.status_code == status


# Operations with delete company
@pytest.mark.parametrize("status", [
    204,
    400,  # user don't have company
    403  # not enough rights
])
def test_delete_company(get_user, status, five_new_users):
    if status == 403:
        get_user = five_new_users[-1]["token"]
    headers = {'content-type': 'application/json', 'Authorization': f'Bearer {get_user}'}
    response = requests.delete(f"{base_url}/company/", headers=headers)
    assert response.status_code == status
