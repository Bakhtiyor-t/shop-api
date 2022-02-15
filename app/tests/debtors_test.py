import json
from uuid import uuid4

import pytest

from app.database.schemas.debtors_schemas import Debtor
from app.tests.basic_operations import BasicOperations
from app.tests.config import base_url, admin_user

# this is needed for the authorization fixture, don't delete!
user_data = admin_user
debtor_item = {"name": f"Baxti{uuid4()}", "paid": 123.45, "debt": 465}

# the number of records created must be equal
# to the number of records updated and deleted
data_array = [
    (debtor_item, 200),
    ({"names": 46}, 422),
    (debtor_item, 400)  # user don't have company
]

# It's need for test work
basic_operations = BasicOperations()


@pytest.mark.parametrize("status", [
    200, 400
])
def test_get_debtors(token, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="debtors/",
        schema=Debtor
    )
    basic_operations.get_items()


@pytest.mark.parametrize("data, status", data_array)
def test_create_debtor(token, data, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="debtors/",
        schema=Debtor
    )
    basic_operations.create_items(data=json.dumps(data))


@pytest.mark.parametrize("data, status", data_array)
def test_update_debtor(token, data, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="debtors/{item_id}/",
        schema=Debtor
    )
    basic_operations.update_items(data=json.dumps(data))


@pytest.mark.parametrize("status", [
    204, 400  # user don't have company
])
def test_delete_debtor(token, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="debtors/{item_id}/",
        schema=Debtor
    )
    basic_operations.delete_items()
