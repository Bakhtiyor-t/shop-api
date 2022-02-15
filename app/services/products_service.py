from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.operators import ilike_op

from app.database.database import get_session
from app.database.models import tables
from app.database.schemas.products_schemas import ProductCreate
from app.services.dublicated_operations import check_user


class ProductsService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_products(
            self,
            user_id: int
    ) -> List[tables.Product]:
        user = check_user(self.session, user_id)
        products = (
            self.session
                .query(tables.Product)
                .filter_by(company_id=user.company_id)
                .all()
        )
        return products

    def search_product(
            self,
            user_id: int,
            product_name: str
    ) -> List[tables.Product]:
        user = check_user(self.session, user_id)
        product = (
            self.session
            .query(tables.Product)
            .filter_by(company_id=user.company_id)
            .where(ilike_op(tables.Product.name, f'%{product_name}%'))
            # .where(tables.Product.name.contains(product_name))
            .all()
        )
        return product
