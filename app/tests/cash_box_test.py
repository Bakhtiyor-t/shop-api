import json
from datetime import datetime

import pytest

from app.database.schemas.cash_box_schemas import CashBox
# this is needed for the authorization fixture, don't delete!
from app.tests.basic_operations import BasicOperations
from app.tests.config import base_url, admin_user

user_data = admin_user
item_data = {"cash": "123000.0", "card": "130000.0", "date": f"{datetime.now()}"}
# the number of records created must be equal
# to the number of records updated and deleted
data_array = [
    (item_data, 200),
    ({"cash": 123}, 422),  # invalid data
    (item_data, 400),  # user don't have company
]

# It's need for test work
basic_operations = BasicOperations()


@pytest.mark.parametrize("status", [
    200,
    400,  # user don't have company
])
def test_get_cash_box(token, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="cash_box/",
        schema=CashBox
    )
    basic_operations.get_items()


@pytest.mark.parametrize("data, status", data_array)
def test_create_cash_box(token, data, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="cash_box/",
        schema=CashBox
    )
    basic_operations.create_items(data=json.dumps(data))


@pytest.mark.parametrize("data, status", data_array)
def test_update_cash_box(token, data, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="cash_box/{item_id}/",
        schema=CashBox
    )
    basic_operations.update_items(data=json.dumps(data))


@pytest.mark.parametrize("status", [
    204, 400
])
def test_delete_cash_box(token, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="cash_box/{item_id}/",
        schema=CashBox
    )
    basic_operations.delete_items()
