import unittest

import requests as req


# Write your token down here.
TOKEN = ""


class TestYaDiskAPI(unittest.TestCase):
    HEADERS = {"Authorization": "OAuth " + TOKEN, "Content-Type": "application/json"}
    URL = r"https://cloud-api.yandex.net/"
    PARAMS = {"path": "test_folder"}

    def setUp(self) -> None:
        # Trying to delete the folder if it already exists (e.g. after training on Yandex Poligon)."
        deletion_req_url = self.URL + "v1/disk/resources"
        req.delete(deletion_req_url, params=self.PARAMS, headers=self.HEADERS)

    def test_create_folder_on_yandex_disk(self):
        folder_creation_url = self.URL + "v1/disk/resources"
        response = req.put(folder_creation_url, params=self.PARAMS, headers=self.HEADERS)
        assert response.status_code == 201

    def tearDown(self) -> None:
        deletion_req_url = self.URL + "v1/disk/resources"
        req.delete(deletion_req_url, params=self.PARAMS, headers=self.HEADERS)
