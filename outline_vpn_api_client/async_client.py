import json
from datetime import datetime
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
    Checks the response from the Outline VPN server for errors and raises an exception
    if the request was not successful.

    Args:
        response (httpx.Response): The HTTP response object returned from a request to the Outline VPN server.
        json (dict, optional): The JSON data from the response to use in the error message. If not provided,
                               it will attempt to parse the response body to retrieve the error message.

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

    Provides common functionality for making HTTP requests to the Outline server API.
    Designed to be inherited by other classes that interact with specific API endpoints.

    Args:
        management_url (str): The management URL used to communicate with the Outline server API.
        ssl_verify (bool, optional): Flag to enable or disable SSL certificate verification. Default is False.
                                     Set to False if the server uses a self-signed certificate.
    """

    def __init__(self, management_url: str, ssl_verify: bool = False):
        self.base_url = f"{management_url}"
        self.ssl_verify = ssl_verify


class AsyncServer(AsyncBaseRoute):
    """
    A class for managing the Outline VPN server's settings and configurations asynchronously.

    Provides methods to interact with and configure server-level settings such as renaming the server,
    changing the hostname, adjusting port settings, and setting or removing data transfer limits.

    Args:
        management_url (str): The management URL used to communicate with the Outline server API.
        ssl_verify (bool, optional): Flag to enable or disable SSL certificate verification. Default is False.
    """

    async def get_information(self) -> models.Server:
        """
        Returns information about the server.

        Returns:
            models.Server: Server configuration and state.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.get(f"{self.base_url}/server")
            response_json = response.json()
            _check_response(response, response_json)
        return models.Server.model_validate(response_json)

    async def change_hostname(self, hostname: str) -> bool:
        """
        Changes the hostname for access keys.

        Updates the hostname or IP address used for access keys on the Outline VPN server.
        If a hostname is provided, DNS must be configured independently of this API.

        Args:
            hostname (str): The new hostname or IP address to use for access keys.

        Returns:
            bool: True if the hostname was successfully changed.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        data = {"hostname": hostname}
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.put(f"{self.base_url}/server/hostname-for-access-keys", json=data)
            _check_response(response)
        return True

    async def rename(self, name: str) -> bool:
        """
        Renames the server.

        Args:
            name (str): The new name for the server.

        Returns:
            bool: True if the server was successfully renamed.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        data = {"name": name}
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.put(f"{self.base_url}/name", json=data)
            _check_response(response)
        return True

    async def change_default_port_for_new_keys(self, port: int) -> bool:
        """
        Changes the default port for newly created access keys.

        The specified port can be one already in use by other access keys.

        Args:
            port (int): The new default port to be used for newly created access keys.

        Returns:
            bool: True if the default port was successfully changed.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        data = {"port": port}
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.put(f"{self.base_url}/server/port-for-new-access-keys", json=data)
            _check_response(response)
        return True

    async def set_server_default_limits(self, limit: int) -> bool:
        """
        Sets a data transfer limit for all access keys.

        Args:
            limit (int): The data transfer limit in bytes to set for all access keys.

        Returns:
            bool: True if the default data transfer limit was successfully set.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        data = {"limit": {"bytes": limit}}
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.put(f"{self.base_url}/server/access-key-data-limit", json=data)
            _check_response(response)
        return True

    async def remove_server_default_limits(self) -> bool:
        """
        Removes the access key data limit, lifting data transfer restrictions on all access keys.

        Returns:
            bool: True if the data transfer limit was successfully removed.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.delete(f"{self.base_url}/server/access-key-data-limit")
            _check_response(response)
        return True

    def __str__(self):
        return json.dumps({"info": "AsyncServer object for managing server settings"}, ensure_ascii=False)


class AsyncMetrics(AsyncBaseRoute):
    """
    A class for interacting with the Outline VPN server's metrics API asynchronously.

    Provides methods to check whether metrics collection is enabled, toggle it,
    retrieve per-key data transfer statistics, and fetch detailed experimental server metrics.

    Args:
        management_url (str): The management URL used to communicate with the Outline server API.
        ssl_verify (bool, optional): Flag to enable or disable SSL certificate verification. Default is False.
    """

    def __init__(self, management_url, ssl_verify=False):
        super().__init__(management_url, ssl_verify)
        self.base_url = f"{self.base_url}/metrics"

    async def check_enabled(self) -> bool:
        """
        Returns whether metrics collection is enabled on the Outline VPN server.

        Returns:
            bool: True if metrics collection is enabled, False otherwise.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.get(f"{self.base_url}/enabled")
            response_json = response.json()
            _check_response(response, response_json)
        return response_json.get("metricsEnabled")

    async def change_enabled_state(self, state: bool = False) -> bool:
        """
        Enables or disables the sharing of metrics on the Outline VPN server.

        Args:
            state (bool): True to enable metrics sharing, False to disable. Default is False.

        Returns:
            bool: True if the metrics sharing state was successfully updated.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        data = {"metricsEnabled": state}
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.put(f"{self.base_url}/enabled", json=data)
            _check_response(response)
        return True

    async def get_data_transfer(self) -> models.BytesTransferredByUserId:
        """
        Returns the data transferred per access key on the Outline VPN server.

        Returns:
            models.BytesTransferredByUserId: Data transfer information for each access key.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.get(f"{self.base_url}/transfer")
            response_json = response.json()
            _check_response(response, response_json)
        return models.BytesTransferredByUserId.model_validate(response_json)

    async def get_server_metrics(self, since: datetime) -> models.ServerMetrics:
        """
        Returns detailed server metrics including tunnel time, data transferred,
        bandwidth, locations, and per-access-key statistics.

        This is an experimental endpoint (`GET /experimental/server/metrics`).
        Note: the endpoint and its response format may change in future server versions.

        Args:
            since (datetime): The start of the time range for which to return metrics.
                              Must be a timezone-aware datetime object.

        Returns:
            models.ServerMetrics: Detailed server and per-key metrics.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).

        Example:
            ```python
            from datetime import datetime, timezone, timedelta

            metrics = await client.metrics.get_server_metrics(
                since=datetime.now(timezone.utc) - timedelta(days=30)
            )
            print(metrics.server.dataTransferred.bytes)
            ```
        """
        since_str = since.strftime("%Y-%m-%dT%H:%M:%SZ")
        base = self.base_url.replace("/metrics", "")
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.get(
                f"{base}/experimental/server/metrics",
                params={"since": since_str},
            )
            response_json = response.json()
            _check_response(response, response_json)
        return models.ServerMetrics.model_validate(response_json)

    def __str__(self):
        return json.dumps({"info": "AsyncMetrics object for managing server metrics"}, ensure_ascii=False)


class AsyncAccessKeys(AsyncBaseRoute):
    """
    A class for managing access keys on the Outline VPN server asynchronously.

    Provides methods to retrieve, create, rename, delete, and set data limits
    on access keys, which are used to control access to the Outline VPN server.

    Args:
        management_url (str): The management URL used to communicate with the Outline server API.
        ssl_verify (bool, optional): Flag to enable or disable SSL certificate verification. Default is False.
    """

    def __init__(self, management_url, ssl_verify=False):
        super().__init__(management_url, ssl_verify)
        self.base_url = f"{self.base_url}/access-keys"

    async def get_all(self) -> models.AccessKeyList:
        """
        Lists all the access keys on the Outline VPN server.

        Returns:
            models.AccessKeyList: All access keys on the server.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.get(f"{self.base_url}")
            response_json = response.json()
            _check_response(response, response_json)
        return models.AccessKeyList.model_validate(response_json)

    async def get(self, id: int) -> models.AccessKey:
        """
        Retrieves the details of a specific access key.

        Args:
            id (int): The ID of the access key to retrieve.

        Returns:
            models.AccessKey: Details of the requested access key.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.get(f"{self.base_url}/{id}")
            response_json = response.json()
            _check_response(response, response_json)
        return models.AccessKey.model_validate(response_json)

    async def create(
        self,
        name: str,
        method: str = "aes-192-gcm",
        password: Optional[str] = None,
        port: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> models.AccessKey:
        """
        Creates a new access key on the Outline VPN server.

        Args:
            name (str): The name to assign to the new access key.
            method (str, optional): The encryption method to use for the access key. Default is "aes-192-gcm".
            password (str, optional): A custom password for the access key. If not provided, the server generates one.
            port (int, optional): A custom port for the access key. If not provided, the server default port is used.
            limit (int, optional): The data transfer limit for the access key in bytes. If not provided, the key will
                                   have no transfer limit.

        Returns:
            models.AccessKey: The newly created access key.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        data = {"name": name, "method": method}
        if password is not None:
            data["password"] = password
        if port is not None:
            data["port"] = port
        if limit is not None:
            data["limit"] = {"bytes": limit}
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.post(f"{self.base_url}", json=data)
            response_json = response.json()
            _check_response(response, response_json)
        return models.AccessKey.model_validate(response_json)

    async def create_with_special_id(
        self,
        id: int,
        name: str,
        method: str = "aes-192-gcm",
        password: Optional[str] = None,
        port: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> models.AccessKey:
        """
        Creates a new access key with a specific identifier.

        Args:
            id (int): The custom ID to assign to the new access key.
            name (str): The name to assign to the new access key.
            method (str, optional): The encryption method to use for the access key. Default is "aes-192-gcm".
            password (str, optional): A custom password for the access key. If not provided, the server generates one.
            port (int, optional): A custom port for the access key. If not provided, the server default port is used.
            limit (int, optional): The data transfer limit for the access key in bytes. If not provided, the key will
                                   have no transfer limit.

        Returns:
            models.AccessKey: The newly created access key.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        data = {"name": name, "method": method}
        if password is not None:
            data["password"] = password
        if port is not None:
            data["port"] = port
        if limit is not None:
            data["limit"] = {"bytes": limit}
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.put(f"{self.base_url}/{id}", json=data)
            response_json = response.json()
            _check_response(response, response_json)
        return models.AccessKey.model_validate(response_json)

    async def delete(self, id: int) -> bool:
        """
        Deletes an access key on the Outline VPN server.

        Args:
            id (int): The ID of the access key to be deleted.

        Returns:
            bool: True if the access key was successfully deleted.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.delete(f"{self.base_url}/{id}")
            _check_response(response)
        return True

    async def rename(self, id: int, name: str) -> bool:
        """
        Renames an existing access key.

        Args:
            id (int): The ID of the access key to be renamed.
            name (str): The new name to assign to the access key.

        Returns:
            bool: True if the access key was successfully renamed.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        data = {"name": name}
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.put(f"{self.base_url}/{id}/name", json=data)
            _check_response(response)
        return True

    async def change_data_limit(self, id: int, limit: int) -> bool:
        """
        Sets a data transfer limit for the specified access key.

        Args:
            id (int): The ID of the access key.
            limit (int): The data transfer limit in bytes.

        Returns:
            bool: True if the data transfer limit was successfully set.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        data = {"limit": {"bytes": limit}}
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.put(f"{self.base_url}/{id}/data-limit", json=data)
            _check_response(response)
        return True

    async def remove_data_limit(self, id: int) -> bool:
        """
        Removes the data transfer limit on the specified access key.

        Args:
            id (int): The ID of the access key.

        Returns:
            bool: True if the data transfer limit was successfully removed.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        async with httpx.AsyncClient(verify=self.ssl_verify) as client:
            response = await client.delete(f"{self.base_url}/{id}/data-limit")
            _check_response(response)
        return True

    def __str__(self):
        return json.dumps({"info": "AsyncAccessKeys object for managing access keys"}, ensure_ascii=False)


class AsyncOutlineClient:
    """
    An asynchronous client for interacting with an Outline VPN server's API.

    Provides asynchronous access to server management, metrics, and access key functionalities.

    Attributes:
        server (AsyncServer): Manages server-level settings and configurations.
        metrics (AsyncMetrics): Monitors and retrieves server metrics.
        access_keys (AsyncAccessKeys): Manages access keys.

    Args:
        management_url (str): The management URL used to communicate with the Outline server API.
        ssl_verify (bool, optional): Flag to enable or disable SSL certificate verification. Default is False.
    """

    def __init__(self, management_url: str = "https://myoutline.com/SecretPath", ssl_verify: bool = False):
        self.server = AsyncServer(management_url, ssl_verify)
        self.metrics = AsyncMetrics(management_url, ssl_verify)
        self.access_keys = AsyncAccessKeys(management_url, ssl_verify)

    async def get_information(self) -> models.Info:
        """
        Retrieves detailed information about the Outline server, including its
        configuration, metrics status, and access keys.

        Returns:
            models.Info: Server info, metrics status, and list of access keys.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        return models.Info.model_validate({
            "server": await self.server.get_information(),
            "metrics": {"enabled": await self.metrics.check_enabled()},
            "access_keys": await self.access_keys.get_all(),
        })

    def __str__(self):
        return json.dumps({"info": "AsyncOutlineClient for Outline VPN server API"}, ensure_ascii=False)