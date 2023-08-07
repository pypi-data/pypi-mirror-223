import requests

from manageritm_client.manageritm_client import ManagerITMClient


class ManagerITMProxyClient(ManagerITMClient):
    def __init__(self, manageritm_uri):
        super().__init__(manageritm_uri)

    def client(self, port=None, webport=None, har=None):
        data = {}

        if port is not None:
            data["port"] = port

        if webport is not None:
            data["webport"] = webport

        if har is not None:
            data["har"] = har

        result = self._http(requests.post, "/client/proxy", json=data)
        self._client_id = result["client_id"]
        return result
