import json
from datetime import datetime

import pytest

from app.database.schemas.invoice_schemas import Invoice, InvoiceWithImage
from app.tests.basic_operations import BasicOperations
from app.tests.config import admin_user, base_url

user_data = admin_user
invoice_item_without_image = {
    "to_pay": 0,
    "paid": 0,
    "previous_debt": 0,
    "debt": 0,
    "date": "2022-02-09T19:21:35.529091",
    "products": [
        {
            "name": "string",
            "count": 0,
            "price": 0,
            "total_price": 0,
            "type": "string"
        }
    ]
}

# the number of records created must be equal
# to the number of records updated and deleted
data_array_without_image = [
    (invoice_item_without_image, 200),
    ({"asd": "asd"}, 422),
    (invoice_item_without_image, 400)
]

invoice_item_with_image = {
    "to_pay": 123,
    "paid": 123,
    "previous_debt": 123,
    "debt": 123,
    "date": datetime.now()
}
# with open("./test_image.jpeg", "rb") as file:
with open("app/tests/test_image.jpeg", "rb") as file:
    image = file.read()

# the number of records created must be equal
# to the number of records updated and deleted
data_array_with_image = [
    (invoice_item_with_image, 200),
    ({"asd": 123}, 422),
    (invoice_item_with_image, 400)
]

# It's need for test work
basic_operations = BasicOperations()
# id 8 is a static firm id it does not change
firm_id = 1


# Operations without image
@pytest.mark.parametrize("status", [
    200, 400
])
def test_get_invoices_without_image(token, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path=f"firms/{firm_id}/invoices/",
        schema=Invoice
    )
    basic_operations.get_items()


@pytest.mark.parametrize("data, status", data_array_without_image)
def test_create_invoice_without_image(token, data, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path=f"firms/{firm_id}/invoice/",
        schema=Invoice
    )
    basic_operations.create_items(data=json.dumps(data))


@pytest.mark.parametrize("data, status", data_array_without_image)
def test_update_invoice_without_image(token, data, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="firms/invoice/{item_id}/",
        schema=Invoice
    )
    basic_operations.update_items(data=json.dumps(data))
    if status == 400:
        basic_operations.updated_items_ids = []


# Operations with image
@pytest.mark.parametrize("status", [
    200, 400
])
def test_get_invoices_with_image(token, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path=f"firms/{firm_id}/invoices_with_image/",
        schema=InvoiceWithImage
    )
    basic_operations.get_items()


@pytest.mark.parametrize("params, status", data_array_with_image)
def test_create_invoice_with_image(token, params, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path=f"firms/{firm_id}/invoice_with_image/",
        schema=InvoiceWithImage
    )
    basic_operations.create_items(
        params=params,
        files={"file": ("upload_image.jpeg", image, "image/jpeg")}
    )


@pytest.mark.parametrize("params, status", data_array_with_image)
def test_update_invoice_with_image(token, params, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="firms/invoice_with_image/{item_id}/",
        schema=InvoiceWithImage
    )
    basic_operations.update_items(
        params=params,
        files={"file": ("upload_image.jpeg", image, "image/jpeg")}
    )


# General operations with invoice
@pytest.mark.parametrize("status", [
    204, 204, 400
])
def test_delete_invoice(token, status, get_user):
    basic_operations.set_values(
        token=token,
        second_token=get_user,
        status=status,
        url=base_url,
        path="firms/invoice/{item_id}/",
        schema=Invoice
    )
    basic_operations.delete_items()
