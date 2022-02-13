import json
from uuid import uuid4

import pytest

from app.database.schemas.shopping_list_schemas import ShoppingList
from app.tests.basic_operations import BasicOperations
from app.tests.config import admin_user, base_url

# this is needed for the authorization fixture, don't delete!
user_data = admin_user
shopping_list_item = {
    "name": f"string{uuid4()}",
    "purchased": False
}

# the number of records created must be equal
# to the number of records updated and deleted
data_array = [
    (shopping_list_item, 200),
    ({"names": 46}, 422),
    (shopping_list_item, 400)  # user don't have company
]

# It's need for test work
basic_operations = BasicOperations()


@pytest.mark.parametrize("status", [
    200, 400
])
def test_get_shopping_list(token, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="shopping-list/",
        schema=ShoppingList
    )
    basic_operations.get_items()


@pytest.mark.parametrize("data, status", data_array)
def test_create_shopping_list_item(token, data, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="shopping-list/",
        schema=ShoppingList
    )
    basic_operations.create_items(data=json.dumps(data))


@pytest.mark.parametrize("data, status", data_array)
def test_update_shopping_list_item(token, data, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="shopping-list/{item_id}/",
        schema=ShoppingList
    )
    basic_operations.update_items(data=json.dumps(data))


@pytest.mark.parametrize("status", [
    204, 400
])
def test_delete_shopping_list_item(token, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="shopping-list/{item_id}/",
        schema=ShoppingList
    )
    basic_operations.delete_items()
