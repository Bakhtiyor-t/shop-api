import requests
from requests import Response


class BasicOperations:
    def __init__(self):
        self.token = None
        self.status = None
        self.second_token = None
        self.url = None
        self.path = None
        self.schema = None
        # I made sure they don't interfere with each other.
        self.updated_items_ids = []
        self.deleted_items_ids = []

    def set_values(
            self, token: str,
            status: int,
            second_token: str,
            url: str,
            path: str,
            schema
    ):
        self.token = token
        self.status = status
        self.second_token = second_token
        self.url = url
        self.path = path
        self.schema = schema

    def _change_token(self):
        if self.status == 400:
            self.token = self.second_token

    def _get_item_id(self, arr):
        item_id = None
        if arr:
            item_id = arr.pop(0)
            arr.append(item_id)
        return item_id

    def _get_response(self, headers, **kwargs) -> Response:
        return requests.get(f'{self.url}/{self.path}', headers=headers, **kwargs)

    def _post_response(self, headers, **kwargs) -> Response:
        return requests.post(f'{self.url}/{self.path}', headers=headers, **kwargs)

    def _put_response(self, headers, path, **kwargs) -> Response:
        return requests.put(f'{self.url}/{path}', headers=headers, **kwargs)

    def _delete_response(self, headers, path, **kwargs) -> Response:
        return requests.delete(f'{self.url}/{path}', headers=headers, **kwargs)

    def get_items(self, **kwargs):
        self._change_token()
        headers = {'content-type': 'application/json', 'Authorization': f'Bearer {self.token}'}
        response = self._get_response(headers=headers, **kwargs)
        data = response.json()
        assert response.status_code == self.status, \
            f"Messages {response.json()} code {response.status_code} : {self.status}"
        if self.status == 200:
            if not data:
                assert data == []
            else:
                if isinstance(data, list):
                    for item in response.json():
                        assert self.schema.parse_obj(item)
                else:
                    assert self.schema.parse_obj(data)

    def create_items(self, **kwargs):
        self._change_token()
        headers = {'Authorization': f'Bearer {self.token}'}
        response = self._post_response(headers=headers, **kwargs)
        assert response.status_code == self.status, \
            f"Messages {response.json()} code {response.status_code} : {self.status}"
        if self.status == 200:
            assert self.schema.parse_obj(response.json())
            self.updated_items_ids.append(response.json()["id"])
            self.deleted_items_ids.append(response.json()["id"])

    def update_items(self, **kwargs):
        self._change_token()
        headers = {'Authorization': f'Bearer {self.token}'}
        item_id = self._get_item_id(self.updated_items_ids)
        path = self.path.replace("{item_id}", f"{item_id}")
        response = self._put_response(headers=headers, path=path, **kwargs)
        assert response.status_code == self.status, \
            f"Messages {response.json()} code {response.status_code} : {self.status} {item_id} {self.updated_items_ids}"
        if self.status == 200:
            assert self.schema.parse_obj(response.json())

    def delete_items(self, **kwargs):
        self._change_token()
        headers = {'Authorization': f'Bearer {self.token}'}
        item_id = self._get_item_id(self.deleted_items_ids)
        path = self.path.replace("{item_id}", f"{item_id}")
        response = self._delete_response(headers=headers, path=path, **kwargs)
        assert response.status_code == self.status, \
            f"Messages {response.json()} code {response.status_code} : {self.status}"
