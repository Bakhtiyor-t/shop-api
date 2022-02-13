# this is needed for the authorization fixture, don't delete!
import json
from uuid import uuid4

import pytest

from app.database.schemas.firms_schemas import Firm
from app.tests.basic_operations import BasicOperations
from app.tests.config import admin_user, base_url

# this is needed for the authorization fixture, don't delete!
user_data = admin_user

firm_item = {
    "paid": 0,
    "debt": 0,
    "date": "2022-02-09T17:21:04.576Z",
    "name": f"string{uuid4()}"
}

# the number of records created must be equal
# to the number of records updated and deleted
data_array = [
    (firm_item, 200),
    ({"names": 46}, 422),
    (firm_item, 400)  # user don't have company
]

# It's need for test work
basic_operations = BasicOperations()


@pytest.mark.parametrize("status", [
    200, 400
])
def test_get_firms(token, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="firms",
        schema=Firm
    )
    basic_operations.get_items()


@pytest.mark.parametrize("data, status", data_array)
def test_create_firm(token, data, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="firms/",
        schema=Firm
    )
    basic_operations.create_items(data=json.dumps(data))


@pytest.mark.parametrize("data, status", data_array)
def test_update_firm(token, data, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="firms/{item_id}/",
        schema=Firm
    )
    basic_operations.update_items(data=json.dumps(data))


@pytest.mark.parametrize("status", [
    204, 400
])
def test_delete_firm(token, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="firms/{item_id}/",
        schema=Firm
    )
    basic_operations.delete_items()
