import json
from typing import Optional

import requests
from requests.models import Response

from . import models
from .error import ResponseNotOkException

def _get_error_message(status_code: int, error: str) -> str:
        """
        Constructs an error message string based on the status code and error details.

        This helper function is used to format the error message when an API request fails. It creates a string that 
        includes the HTTP status code and the error message received from the server.

        Args:
            status_code (int): The HTTP status code from the server response.
            error (str): The error message returned by the server, typically in JSON format or as a string.

        Returns:
            str: A formatted error message string indicating the error, including the status code and the error description.

        """
        return f"An error occured: {status_code} - {error}"
    
def _check_response(response: Response, json: Optional[str] = None):
    """
    Checks the response from the Outline VPN server for errors and raises an exception if the request was not successful.

    This function is used to validate the server's response. If the response's status code is 300 or higher (indicating 
    an error), it will raise a `ResponseNotOkException` with an appropriate error message.

    Args:
        response (Response): The HTTP response object returned from a request to the Outline VPN server.
        json (str, optional): The JSON data from the response to use in the error message. If not provided, it will 
                              attempt to parse the response body to retrieve the error message.

    Raises:
        ResponseNotOkException: If the response status code is 300 or higher, indicating an error occurred.
    """
    if response.status_code >= 300:
        if not json:
            json = response.json()
        raise ResponseNotOkException(_get_error_message(response.status_code, json))
    
class BaseRoute:
    """
    A base class for handling API routes in the Outline VPN server.

    This class provides common functionality for making HTTP requests to the Outline server API. It is meant to be 
    inherited by other classes (such as `AccessKeys`, `Metrics`, `Server`) that interact with specific API endpoints.

    Attributes:
        base_url (str): The base URL for the API endpoint, which is formed using the provided management URL.
        ssl_verify (bool): A flag to enable or disable SSL certificate verification for API requests. Default is `False`.

    Args:
        management_url (str): The management URL used to communicate with the Outline server API.
        ssl_verify (bool, optional): Flag to enable or disable SSL certificate verification for API requests. Default is `False`.
                        You should set this flag to `False` if the server's SSL certificate is self-signed or if no certificate is present.
    """

    def __init__(self, management_url: str, ssl_verify: bool = False):
        self.base_url = f"{management_url}"
        self.ssl_verify = ssl_verify

class Server(BaseRoute):
    """
    A class for managing the Outline VPN server's settings and configurations.

    This class provides methods to interact with and configure various server-level settings for the Outline VPN server.
    It allows you to perform tasks like renaming the server, changing the hostname, adjusting port settings, 
    and setting or removing data transfer limits for the server.

    Attributes:
        base_url (str): The base URL for the metrics endpoint of the Outline server.

    Args:
        management_url (str): The management URL used to communicate with the Outline server API.
        ssl_verify (bool): Flag to enable or disable SSL certificate verification for API requests. Default is `False`.
                        You should set this flag to `False` if the server's SSL certificate is self-signed or if no certificate is present.
    """
    def __str__(self):
        return json.dumps(self.get_information().model_dump(), ensure_ascii=False, indent=4)

    def get_information(self) -> models.Server:
        """
        Returns information about the server.

        This method retrieves detailed information about the Outline VPN server, such as its status, configuration, 
        and other relevant details.

        Returns:
            dict: A dictionary containing the server information.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        response = requests.get(f"{self.base_url}/server", verify=self.ssl_verify)
        response_json = response.json()
        _check_response(response, response_json)
        return models.Server.model_validate(response_json)
    
    def change_hostname(self, hostname: str) -> bool:
        """
        Changes the hostname for access keys.

        This method updates the hostname or IP address used for access keys on the Outline VPN server. 
        If a hostname is provided, it must be valid and DNS must be configured independently of this API.

        Args:
            hostname (str): The new hostname or IP address to use for access keys.

        Returns:
            bool: Returns `True` if the hostname was successfully changed.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        data = {
            "hostname": hostname
        }
        response = requests.put(f"{self.base_url}/server/hostname-for-access-keys", json=data, verify=self.ssl_verify)
        _check_response(response)
        return True
    
    def rename(self, name: str) -> bool:
        """
        Renames the server.

        This method changes the name of the Outline VPN server to the specified `name`.

        Args:
            name (str): The new name for the server.

        Returns:
            bool: Returns `True` if the server was successfully renamed.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        data = {
            "name": name
        }
        response = requests.put(f"{self.base_url}/name", json=data, verify=self.ssl_verify)
        _check_response(response)
        return True
    
    def change_default_port_for_new_keys(self, port: int) -> bool:
        """
        Changes the default port for newly created access keys.

        This method updates the default port that will be used for new access keys. The specified port can be one
        that is already in use by other access keys.

        Args:
            port (int): The new default port to be used for newly created access keys.

        Returns:
            bool: Returns `True` if the default port was successfully changed.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        data = {
            "port": port
        }
        response = requests.put(f"{self.base_url}/server/port-for-new-access-keys", json=data, verify=self.ssl_verify)
        _check_response(response)
        return True
    
    def set_server_default_limits(self, limit: int) -> bool:
        """
        Sets a data transfer limit for all access keys.

        This method sets a default data transfer limit that will apply to all access keys on the server. 
        The specified limit is in bytes.

        Args:
            limit (int): The data transfer limit in bytes to set for all access keys.

        Returns:
            bool: Returns `True` if the default data transfer limit was successfully set.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        data = {
            "limit": {
                "bytes": limit
            }
        }
        response = requests.put(f"{self.base_url}/server/access-key-data-limit", json=data, verify=self.ssl_verify)
        _check_response(response)
        return True
        
    def remove_server_default_limits(self) -> bool:
        """
        Removes the access key data limit, lifting data transfer restrictions on all access keys.

        This method removes the data transfer limit for all access keys, effectively lifting any restrictions 
        on data usage for the keys.

        Returns:
            bool: Returns `True` if the data transfer limit was successfully removed.

        Raises:
            ResponseNotOkException: If the server response indicates an error (status code >= 300).
        """
        response = requests.delete(f"{self.base_url}/server/access-key-data-limit", verify=self.ssl_verify)
        _check_response(response)
        return True

class Metrics(BaseRoute):
    """
    A class for interacting with the Outline VPN server's metrics API.

    This class provides methods to retrieve and check the status of various server metrics. It allows you to determine
    whether metrics collection is enabled on the server.

    Attributes:
        base_url (str): The base URL for the metrics endpoint of the Outline server, formed by appending "/metrics"
                        to the management URL.

    Args:
        management_url (str): The management URL used to communicate with the Outline server API.
        ssl_verify (bool): Flag to enable or disable SSL certificate verification for API requests. Default is `False`.
                        You should set this flag to `False` if the server's SSL certificate is self-signed or if no certificate is present.
    """
    def __init__(self, management_url, ssl_verify = False):
        super().__init__(management_url, ssl_verify)
        self.base_url = f"{self.base_url}/metrics"

    def __str__(self):
        return json.dumps({'enabled': self.check_enabled()}, ensure_ascii=False, indent=4)

    def check_enabled(self) -> bool:
        """
        Returns whether metrics collection is enabled on the Outline VPN server.

        This method sends a request to the server to check if metrics sharing is currently enabled. 
        It parses the response to determine whether metrics are being shared and returns a boolean indicating the status.

        Returns:
            bool: `True` if metrics collection is enabled, `False` otherwise.

        Raises:
            ResponseNotOkException: If the server responds with a status code indicating an error (status code >= 300).
        """
        response = requests.get(f"{self.base_url}/enabled", verify=self.ssl_verify)
        response_json: dict = response.json()
        _check_response(response)
        return response_json.get("metricsEnabled")

    def change_enabled_state(self, state: bool = False) -> bool:
        """
        Enables or disables the sharing of metrics on the Outline VPN server.

        This method allows you to enable or disable the sharing of metrics. It sends a request to the server to update 
        the state of metrics sharing based on the provided `state` parameter.

        Args:
            state (bool): A boolean indicating whether to enable (`True`) or disable (`False`) metrics sharing. Default is `False`.

        Returns:
            bool: `True` if the metrics sharing state was successfully updated.

        Raises:
            ResponseNotOkException: If the server responds with a status code indicating an error (status code >= 300).
        """
        data = {
            "metricsEnabled": state
        }
        response = requests.put(f"{self.base_url}/enabled", json=data, verify=self.ssl_verify)
        _check_response(response)
        return True
    
    def get_data_transfer(self) -> models.BytesTransferredByUserId:
        """
        Returns the data transferred per access key on the Outline VPN server.

        This method retrieves information about the amount of data transferred for each access key.
        It sends a request to the server to fetch the data transfer details and returns a dictionary containing 
        the transfer data.

        Returns:
            dict: A dictionary containing data transfer information for each access key.

            The returned dictionary contains the following format:
            {
                "bytesTransferredByUserId": {
                    "user_id_1": data_in_bytes,
                    "user_id_2": data_in_bytes,
                    ...
                }
            }

            Where `user_id_1`, `user_id_2`, etc. are the access key IDs (user IDs), and `data_in_bytes` represents 
            the amount of data transferred by the corresponding access key in bytes.

        Raises:
            ResponseNotOkException: If the server responds with a status code indicating an error (status code >= 300).
        """
        response = requests.get(f"{self.base_url}/transfer", verify=self.ssl_verify)
        response_json = response.json()
        _check_response(response, response_json)
        return models.BytesTransferredByUserId.model_validate(response_json)

class AccessKeys(BaseRoute):
    """
    A class for managing access keys on the Outline VPN server.

    This class provides methods to interact with the Outline server's access keys API. It allows you to retrieve,
    create, and manage access keys, which are used to control access to the Outline VPN server.
    
    Attributes:
        base_url (str): The base URL for the access keys endpoint of the Outline server, formed by appending "/access-keys"
                        to the management URL.

    Args:
        management_url (str): The management URL used to communicate with the Outline server API.
        ssl_verify (bool): Flag to enable or disable SSL certificate verification for API requests. Default is `False`.
                        You should set this flag to `False` if the server's SSL certificate is self-signed or if no certificate is present.
    """
    def __init__(self, management_url, ssl_verify = False):
        super().__init__(management_url, ssl_verify)
        self.base_url = f"{self.base_url}/access-keys"

    def __str__(self):
        return json.dumps(self.get_all().model_dump(), ensure_ascii=False, indent=4)

    def get_all(self) -> models.AccessKeyList:
        """
        Lists all the access keys on the Outline VPN server.

        This method sends a request to the server to retrieve a list of all access keys that are currently created.
        It returns a dictionary containing the details of all access keys.

        Returns:
            dict: A dictionary containing the details of all access keys, including their IDs and other related information.

        Raises:
            ResponseNotOkException: If the server responds with a status code indicating an error (status code >= 300).        
        """
        response = requests.get(self.base_url, verify=self.ssl_verify)
        response_json = response.json()
        _check_response(response, response_json)
        return models.AccessKeyList.model_validate(response_json)
    
    def get(self, id: int) -> models.AccessKey:
        """
        Retrieves the details of a specific access key on the Outline VPN server.

        This method sends a request to the server to retrieve the information of a single access key, identified by its ID.

        Args:
            id (int): The ID of the access key to retrieve.

        Returns:
            dict: A dictionary containing the details of the requested access key, including its ID, name, creation date, 
                and other relevant information.

        Raises:
            ResponseNotOkException: If the server responds with a status code indicating an error (status code >= 300).
        """
        response = requests.get(f"{self.base_url}/{id}", verify=self.ssl_verify)
        response_json = response.json()
        _check_response(response, response_json)
        return models.AccessKey.model_validate(response_json)
    
    def create(self, name: str, method: str = "aes-192-gcm", limit: Optional[int] = None) -> models.AccessKey:
        """
        Creates a new access key on the Outline VPN server.

        This method sends a request to the server to create a new access key. You can specify the name of the key, the 
        encryption method to use, and optionally set a data transfer limit for the key. If no limit is provided, the key 
        will have no data transfer restrictions.

        Args:
            name (str): The name to assign to the new access key.
            method (str, optional): The encryption method to use for the access key. Default is "aes-192-gcm".
            limit (int, optional): The data transfer limit for the access key in megabytes. If not provided, the key will 
                                have no transfer limit.

        Returns:
            dict: A dictionary containing the details of the newly created access key, including its ID, name and any other relevant information.

        Raises:
            ResponseNotOkException: If the server responds with a status code indicating an error (status code >= 300).
        """
        data = {
            "name": name,
            "method": method,
        }
        if limit:
            data['limit'] = {
                "bytes": limit
            }
        response = requests.post(f"{self.base_url}", json=data, verify=self.ssl_verify)
        response_json = response.json()
        _check_response(response, response_json)
        return  models.AccessKey.model_validate(response_json)
    
    def create_with_special_id(self, id: int, name: str, method: str = "aes-192-gcm", limit: Optional[int] = None) -> models.AccessKey:
        """
        Creates a new access key on the Outline VPN server with a specific identifier.

        This method sends a request to the server to create a new access key, allowing you to specify a custom ID for 
        the key, along with the key's name, encryption method, and an optional data transfer limit. If no limit is provided, 
        the key will have no data transfer restrictions.

        Args:
            id (int): The custom ID to assign to the new access key.
            name (str): The name to assign to the new access key.
            method (str, optional): The encryption method to use for the access key. Default is "aes-192-gcm".
            limit (int, optional): The data transfer limit for the access key in megabytes. If not provided, the key will 
                                have no transfer limit.

        Returns:
            dict: A dictionary containing the details of the newly created access key, including its ID, name, creation 
                date, encryption method, transfer limit, and other relevant information.

        Raises:
            ResponseNotOkException: If the server responds with a status code indicating an error (status code >= 300).
        """
        data = {
            "name": name,
            "method": method,
        }
        if limit:
            data['limit'] = {
                "bytes": limit
            }
        response = requests.put(f"{self.base_url}/{id}", json=data, verify=self.ssl_verify)
        response_json = response.json()
        _check_response(response, response_json)
        return models.AccessKey.model_validate(response_json)
    
    def delete(self, id: int) -> bool:
        """
         Deletes an access key on the Outline VPN server.

        This method sends a request to the server to delete a specific access key identified by its ID. Deleting an access 
        key will revoke its access to the VPN server.

        Args:
            id (int): The ID of the access key to be deleted.

        Returns:
            bool: `True` if the access key was successfully deleted.

        Raises:
            ResponseNotOkException: If the server responds with a status code indicating an error (status code >= 300).

        """
        response = requests.delete(f"{self.base_url}/{id}", verify=self.ssl_verify)
        _check_response(response)
        return True
    
    def rename(self, id: int, name: str) -> bool:
        """
        Renames an existing access key on the Outline VPN server.

        This method sends a request to the server to rename a specific access key identified by its ID. The new name for 
        the access key is provided as an argument.

        Args:
            id (int): The ID of the access key to be renamed.
            name (str): The new name to assign to the access key.

        Returns:
            bool: `True` if the access key was successfully renamed.

        Raises:
            ResponseNotOkException: If the server responds with a status code indicating an error (status code >= 300).
        """
        data = {
            "name": name
        }
        response = requests.put(f"{self.base_url}/{id}/name", json=data, verify=self.ssl_verify)
        _check_response(response)
        return True
    
    def change_data_limit(self, id: int, limit: int) -> bool:
        """
        Sets a data transfer limit for the specified access key on the Outline VPN server.

        This method sends a request to the server to apply a data transfer limit for a specific access key, identified 
        by its ID. The limit is specified in megabytes (MB). If the specified limit is set to `None`, it removes the 
        data transfer restriction for the key.

        Args:
            id (int): The ID of the access key for which the data transfer limit will be set.
            limit (int): The data transfer limit in megabytes (MB) to apply to the access key. A value of `None` removes 
                        any data transfer limits.

        Returns:
            bool: `True` if the data transfer limit was successfully set for the access key.

        Raises:
            ResponseNotOkException: If the server responds with a status code indicating an error (status code >= 300).
        """
        data = {
            "limit": {
                "bytes": limit
            }
        }
        response = requests.put(f"{self.base_url}/{id}/data-limit", json=data, verify=self.ssl_verify)
        _check_response(response)
        return True
    
    def remove_data_limit(self, id: int) -> bool:
        """
        Removes the data transfer limit on the specified access key on the Outline VPN server.

        This method sends a request to the server to remove the data transfer limit for a specific access key, identified 
        by its ID. After calling this method, the access key will no longer have any data transfer restrictions.

        Args:
            id (int): The ID of the access key for which the data transfer limit will be removed.

        Returns:
            bool: `True` if the data transfer limit was successfully removed for the access key.

        Raises:
            ResponseNotOkException: If the server responds with a status code indicating an error (status code >= 300).
        """
        response = requests.delete(f"{self.base_url}/{id}/data-limit", verify=self.ssl_verify)
        _check_response(response)
        return True

class OutlineClient:
    """
    A client for interacting with an Outline VPN server's API.

    This class provides access to the server management, metrics, and access keys functionalities of the Outline VPN API.
    It allows you to manage server settings, retrieve server information, and interact with access keys and metrics.

    Attributes:
        server (Server): An instance of the `Server` class for managing server-level settings and configurations.
        metrics (Metrics): An instance of the `Metrics` class for monitoring and retrieving server metrics.
        access_keys (AccessKeys): An instance of the `AccessKeys` class for managing and retrieving access keys.

    Args:
        management_url (str): The management URL used to communicate with the Outline server API. Default is 'https://myoutline.com/SecretPath'.
        ssl_verify (bool): Flag to enable or disable SSL certificate verification for API requests. Default is `False`. 
                            You should set this flag to `False` if the server's SSL certificate is self-signed or if no certificate is present.
    """
    def __init__(
        self, 
        management_url: str = 'https://myoutline.com/SecretPath',
        ssl_verify: bool = False
    ):
        self.server = Server(management_url, ssl_verify)
        self.metrics = Metrics(management_url, ssl_verify)
        self.access_keys = AccessKeys(management_url, ssl_verify)

    def __str__(self):
        return json.dumps(self.get_information().model_dump(), ensure_ascii=False, indent=4)
    
    def get_information(self) -> models.Info:
        """
        Retrieves detailed information about the Outline server, including its configuration, metrics, and access keys.

        This method returns a dictionary containing:
            - Information about the server (via the `server.get_information()` method),
            - The status of the metrics (whether they are enabled, checked via the `metrics.check_enabled()` method),
            - A list of all access keys (retrieved using the `access_keys.get_all()` method).

        Returns:
            dict: A dictionary containing:

                - `server`: Information about the server configuration.

                - `metrics`: A dictionary with the status of metrics (e.g., if they are enabled).

                - `access_keys`: A list of all access keys.
        """
        return models.Info.model_validate({
            "server": self.server.get_information(),
            "metrics": {
                "enabled": self.metrics.check_enabled()
            },
            "access_keys": self.access_keys.get_all()
        })