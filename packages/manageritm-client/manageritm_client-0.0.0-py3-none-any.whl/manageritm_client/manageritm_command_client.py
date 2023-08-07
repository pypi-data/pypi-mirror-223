import requests

from manageritm_client.manageritm_client import ManagerITMClient


class ManagerITMCommandClient(ManagerITMClient):
    def __init__(self, manageritm_uri):
        super().__init__(manageritm_uri)

    def client(self, env=None, additional_env=None):
        data = {}

        if env is not None:
            data["env"] = env

        if additional_env is not None:
            data["additional_env"] = additional_env

        result = self._http(requests.post, "/client/command", json=data)
        self._client_id = result["client_id"]
        return result
