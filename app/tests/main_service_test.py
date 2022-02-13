import requests

from app.database.schemas.main_schemas import Report
from app.tests.config import base_url, admin_user

user_data = admin_user


def test_get_info(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{base_url}/main/", headers=headers)
    assert response.status_code == 200
    assert Report.parse_obj(response.json())
