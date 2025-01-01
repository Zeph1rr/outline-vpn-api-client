import json
from typing import Optional


from . import models
from .error import ResponseNotOkException

try:
    import httpx
except ImportError:
    raise ImportError(
        "httpx is required for asynchronous functionality. "
        "Install it using 'poetry add outline-vpn-api-client[async]'"
    )


def _get_error_message(status_code: int, error: str) -> str:
    return f"An error occurred: {status_code} - {error}"

def _check_response(response: httpx.Response, json: Optional[dict] = None):
    """
    Checks the response from the Outline VPN server for errors and raises an exception if the request was not successful.

    This function is used to validate the server's response. If the response's status code is 300 or higher (indicating 
    an error), it will raise a `ResponseNotOkException` with an appropriate error message.

    Args:
        response (httpx.Response): The HTTP response object returned from a request to the Outline VPN server.
        json (dict, optional): The JSON data from the response to use in the error message. If not provided, it will 
                              attempt to parse the response body to retrieve the error message.

    Raises:
        ResponseNotOkException: If the response status code is 300 or higher, indicating an error occurred.
    """
    if response.status_code >= 300:
        if not json:
            json = response.json()
        raise ResponseNotOkException(_get_error_message(response.status_code, json))

class AsyncBaseRoute:
    """
    Base class for asynchronous API interaction.

    This class provides common functionality for making HTTP requests to the Outline server API.
    It is designed to be inherited by other classes that interact with specific API endpoints.

    Attributes:
        base_url (str): The base URL for the API endpoint, formed using the provided management URL.
        ssl_verify (bool): A flag to enable or disable SSL certificate verification for API requests. Default is `False`.
    """
    def __init__(self, management_url: str, ssl_verify: bool = False):
        self.base_url = f"{management_url}"
        self.ssl_verify = ssl_verify

class AsyncServer(AsyncBaseRoute):
    """
    A class for managing the Outline VPN server's settings and configurations asynchronously.

    This class provides methods to interact with and configure various server-level settings for the Outline VPN server.
    It allows you to perform tasks like renaming the server, changing the hostname, adjusting port settings, 
    and setting or removing data transfer limits for the server.

    Methods:
        get_information() -> dict:
            Retrieves detailed information about the server.

        change_hostname(hostname: str) -> bool:
            Changes the hostname for access keys.

        rename(name: str) -> bool:
            Renames the server.

        change_default_port_for_new_keys(port: int) -> bool:
            Changes the default port for newly created access keys.

        set_server_default_limits(limit: int) -> bool:
            Sets a data transfer limit for all access keys.

        remove_server_default_limits() -> bool:
            Removes the data transfer limit for all access keys.
    """

    async def get_information(self) -> models.Server:
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.get(f"{self.base_url}/server")
            response_json = response.json()
            _check_response(response, response_json)
        return models.Server.model_validate(response_json)
    
    async def change_hostname(self, hostname: str) -> bool:
        data = {"hostname": hostname}
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.put(f"{self.base_url}/server/hostname-for-access-keys", json=data)
            _check_response(response)
        return True

    async def rename(self, name: str) -> bool:
        data = {"name": name}
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.put(f"{self.base_url}/name", json=data)
            _check_response(response)
        return True

    async def change_default_port_for_new_keys(self, port: int) -> bool:
        data = {"port": port}
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.put(f"{self.base_url}/server/port-for-new-access-keys", json=data)
            _check_response(response)
        return True

    async def set_server_default_limits(self, limit: int) -> bool:
        data = {"limit": {"bytes": limit}}
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.put(f"{self.base_url}/server/access-key-data-limit", json=data)
            _check_response(response)
        return True

    async def remove_server_default_limits(self) -> bool:
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.delete(f"{self.base_url}/server/access-key-data-limit")
            _check_response(response)
        return True

    def __str__(self):
        return json.dumps({"info": "AsyncServer object for managing server settings"}, ensure_ascii=False)

class AsyncMetrics(AsyncBaseRoute):
    """
    A class for interacting with the Outline VPN server's metrics API asynchronously.

    This class provides methods to retrieve and check the status of various server metrics. It allows you to determine
    whether metrics collection is enabled on the server and retrieve data transfer information.

    Methods:
        check_enabled() -> bool:
            Checks whether metrics collection is enabled on the server.

        change_enabled_state(state: bool) -> bool:
            Enables or disables metrics sharing on the server.

        get_data_transfer() -> dict:
            Retrieves data transfer information per access key.
    """
    def __init__(self, management_url, ssl_verify=False):
        super().__init__(management_url, ssl_verify)
        self.base_url = f"{self.base_url}/metrics"

    async def check_enabled(self) -> bool:
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.get(f"{self.base_url}/enabled")
            response_json = response.json()
            _check_response(response, response_json)
        return response_json.get("metricsEnabled")

    async def change_enabled_state(self, state: bool = False) -> bool:
        data = {"metricsEnabled": state}
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.put(f"{self.base_url}/enabled", json=data)
            _check_response(response)
        return True

    async def get_data_transfer(self) -> models.BytesTransferredByUserId:
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.get(f"{self.base_url}/transfer")
            response_json = response.json()
            _check_response(response, response_json)
        return models.BytesTransferredByUserId.model_validate(response_json)

    def __str__(self):
        return json.dumps({"info": "AsyncMetrics object for managing server metrics"}, ensure_ascii=False)

class AsyncAccessKeys(AsyncBaseRoute):
    """
    A class for managing access keys on the Outline VPN server asynchronously.

    This class provides methods to interact with the Outline server's access keys API. It allows you to retrieve,
    create, and manage access keys, which are used to control access to the Outline VPN server.

    Methods:
        get_all() -> dict:
            Retrieves all access keys on the server.

        get(id: int) -> dict:
            Retrieves details of a specific access key by ID.

        create(name: str, method: str = "aes-192-gcm", limit: Optional[int] = None) -> dict:
            Creates a new access key with optional data transfer limits.

        create_with_special_id(id: int, name: str, method: str = "aes-192-gcm", limit: Optional[int] = None) -> dict:
            Creates a new access key with a specified ID and optional limits.

        delete(id: int) -> bool:
            Deletes an access key by its ID.

        rename(id: int, name: str) -> bool:
            Renames an access key.

        change_data_limit(id: int, limit: int) -> bool:
            Sets a data limit for an access key.

        remove_data_limit(id: int) -> bool:
            Removes the data limit for an access key.
    """
    def __init__(self, management_url, ssl_verify=False):
        super().__init__(management_url, ssl_verify)
        self.base_url = f"{self.base_url}/access-keys"


    async def get_all(self) -> models.AccessKeyList:
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.get(f"{self.base_url}")
            response_json = response.json()
            _check_response(response, response_json)
        return models.AccessKeyList.model_validate(response_json)

    async def get(self, id: int) -> models.AccessKey:
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.get(f"{self.base_url}/{id}")
            response_json = response.json()
            _check_response(response, response_json)
        return models.AccessKey.model_validate(response_json)

    async def create(self, name: str, method: str = "aes-192-gcm", limit: Optional[int] = None) -> models.AccessKey:
        data = {"name": name, "method": method}
        if limit:
            data["limit"] = {"bytes": limit}
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.post(f"{self.base_url}", json=data)
            response_json = response.json()
            _check_response(response, response_json)
        return  models.AccessKey.model_validate(response_json)


    async def create_with_special_id(self, id: int, name: str, method: str = "aes-192-gcm", limit: Optional[int] = None) -> models.AccessKey:
        data = {"name": name, "method": method}
        if limit:
            data["limit"] = {"bytes": limit}
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.put(f"{self.base_url}/{id}", json=data)
            response_json = response.json()
            _check_response(response, response_json)
        return models.AccessKey.model_validate(response_json)

    async def delete(self, id: int) -> bool:
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.delete(f"{self.base_url}/{id}")
            _check_response(response)
        return True

    async def rename(self, id: int, name: str) -> bool:
        data = {"name": name}
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.put(f"{self.base_url}/{id}/name", json=data)
            _check_response(response)
        return True

    async def change_data_limit(self, id: int, limit: int) -> bool:
        data = {"limit": {"bytes": limit}}
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.put(f"{self.base_url}/{id}/data-limit", json=data)
            _check_response(response)
        return True

    async def remove_data_limit(self, id: int) -> bool:
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.delete(f"{self.base_url}/{id}/data-limit")
            _check_response(response)
        return True

    def __str__(self):
        return json.dumps({"info": "AsyncAccessKeys object for managing access keys"}, ensure_ascii=False)

class AsyncOutlineClient:
    """
    An asynchronous client for interacting with an Outline VPN server's API.

    This class provides asynchronous access to the server management, metrics, and access keys functionalities
    of the Outline VPN API. It allows you to manage server settings, retrieve server information, and interact
    with access keys and metrics.

    Attributes:
        server (AsyncServer): An instance of the `AsyncServer` class for managing server-level settings and configurations.
        metrics (AsyncMetrics): An instance of the `AsyncMetrics` class for monitoring and retrieving server metrics.
        access_keys (AsyncAccessKeys): An instance of the `AsyncAccessKeys` class for managing and retrieving access keys.

    Methods:
        get_information() -> dict:
            Retrieves detailed information about the server, including server settings, metrics status, and access keys.
    """
    def __init__(self, management_url: str = 'https://myoutline.com/SecretPath', ssl_verify: bool = False):
        self.server = AsyncServer(management_url, ssl_verify)
        self.metrics = AsyncMetrics(management_url, ssl_verify)
        self.access_keys = AsyncAccessKeys(management_url, ssl_verify)

    async def get_information(self) -> models.Info:
        """
        Retrieves detailed information about the Outline server, including its configuration, metrics, and access keys.

        Returns:
            dict: A dictionary containing:
                - `server`: Information about the server configuration.
                - `metrics`: A dictionary with the status of metrics (e.g., if they are enabled).
                - `access_keys`: A list of all access keys.
        """
        return models.Info.model_validate({
            "server": await self.server.get_information(),
            "metrics": {"enabled": await self.metrics.check_enabled()},
            "access_keys": await self.access_keys.get_all(),
        })

    def __str__(self):
        return json.dumps({"info": "AsyncOutlineClient for Outline VPN server API"}, ensure_ascii=False)
