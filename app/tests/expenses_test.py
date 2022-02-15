import json
from uuid import uuid4

import pytest

from app.database.schemas.expenses_schemas import Expense
from app.tests.basic_operations import BasicOperations
from app.tests.config import base_url, admin_user

# this is needed for the authorization fixture, don't delete!
user_data = admin_user
expense_item = {
    "firm_id": 0,
    "firm_flag": False,
    "name": f"string{uuid4()}",
    "price": 0,
    "date": "2022-02-09T15:26:56.183466"
}

# the number of records created must be equal
# to the number of records updated and deleted
data_array = [
    (expense_item, 200),
    ({"names": 46}, 422),
    (expense_item, 400)  # user don't have company
]

# It's need for test work
basic_operations = BasicOperations()


@pytest.mark.parametrize("status", [
    200, 400
])
def test_get_expenses(token, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="expenses/",
        schema=Expense
    )
    basic_operations.get_items()


@pytest.mark.parametrize("data, status", data_array)
def test_create_expense(token, data, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="expenses/",
        schema=Expense
    )
    basic_operations.create_items(data=json.dumps(data))


@pytest.mark.parametrize("data, status", data_array)
def test_update_expense(token, data, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="expenses/{item_id}/",
        schema=Expense
    )
    basic_operations.update_items(data=json.dumps(data))


@pytest.mark.parametrize("status", [
    204, 400  # user don't have company
])
def test_delete_expense(token, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="expenses/{item_id}/",
        schema=Expense
    )
    basic_operations.delete_items()
