import pytest

from app.database.schemas.products_schemas import Product
from app.tests.basic_operations import BasicOperations
from app.tests.config import admin_user, base_url

user_data = admin_user

basic_operations = BasicOperations()


@pytest.mark.parametrize('status', [
    200, 400
])
def test_get_products(token, status, get_user):
    basic_operations.set_values(
        token=token,
        status=status,
        second_token=get_user,
        url=base_url,
        path="products/",
        schema=Product
    )
    basic_operations.get_items()


@pytest.mark.parametrize('product_name, status', [
    ("fanta", 200),
    ("sdkljfls;l", 200),  # not find and return empty []
    ("fanta", 400)  # invalid user
])
def test_search_products(token, get_user, status, product_name):
    basic_operations.set_values(
        token=token,
        status=status,
        second_token=get_user,
        url=base_url,
        path=f"products/search/{product_name}",
        schema=Product
    )
    basic_operations.get_items()
