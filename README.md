# OUTLINE-VPN-API-CLIENT

![PyPI - Version](https://img.shields.io/pypi/v/outline-vpn-api-client?style=plastic)
![PyPI - Format](https://img.shields.io/pypi/format/outline-vpn-api-client?style=plastic)
![GitHub Release](https://img.shields.io/github/v/release/Zeph1rr/outline-vpn-api-client?style=plastic)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Zeph1rr/outline-vpn-api-client/tests.yml?style=plastic&label=tests)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/outline-vpn-api-client?style=plastic)
![GitHub License](https://img.shields.io/github/license/zeph1rr/outline-vpn-api-client?style=plastic)



## DESCRIPTION

This library provides a convenient interface for managing an Outline VPN server in Python using the official Outline Management API. It simplifies server interaction by enabling you to:

- Programmatically manage user keys, including creation, updates, and deletion.
- Monitor server usage and retrieve detailed statistics.
- Configure server settings such as bandwidth limits and access rules.
- Automate routine maintenance and management tasks.

The library is suitable for both individual users and administrators of corporate VPN solutions, helping to streamline server management, save time, and improve operational efficiency.

It is designed with simplicity in mind and features cleanly implemented, well-documented methods.

## INSTALLATION

### Using pip

```
pip install outline-vpn-api-client
```

### Using poetry

```
poetry add outline-vpn-api-client
```

## USAGE


To get started with the library, you need to obtain the `management_url` for your Outline VPN server. Once you have the `management_url`, you can create an instance of the `OutlineClient` class to interact with the server.

### Initializing the Client

```python
from outline_vpn_api_client import OutlineClient

# Replace 'your.management.url' with your actual management URL
management_url = "your.management.url"

# Create an OutlineClient instance
client = OutlineClient(management_url=management_url)
```

### Retrieving Server Information

```python
import json

# Fetch server information and pretty-print it
print(json.dumps(client.get_information(), ensure_ascii=False, indent=4))
```

### Creating Access Keys

#### Creating a Key Without Limits

```python
# Replace 'name' with a meaningful identifier for the key
client.access_keys.create(name="Example Key")
```

#### Creating a Key With a Limit

```python
# Replace 'name' with a meaningful identifier for the key
# Replace 'limit' with the desired bandwidth limit in bytes
client.access_keys.create(name="Example Key with Limit", limit=10**9)  # Example: 1 GB limit
```

### Handling Errors

The library uses a custom exception, ResponseNotOkException, to handle server-side errors. This exception is raised whenever the API returns an unexpected response.

```python
from outline_vpn_api_client import ResponseNotOkException

try:
    # Attempting to fetch server information
    info = client.get_information()
    print(info)
except ResponseNotOkException as e:
    print(e)
```

The error message provides details about the HTTP status code and the error message returned by the API. It follows this format:

```python
def _get_error_message(status_code: int, error: str) -> str:
    return f"An error occurred: {status_code} - {error}"
```

For example, if the API returns a 404 error with the message "Not Found", the exception will produce the message:

```
outline_vpn_api_client.client.ResponseNotOkException: An error occured: 404 - {'code': 'NotFound', 'message': 'Access key "100" not found'}    
```

### Async Usage

For use async client install async version of package:
```
pip install outline-vpn-api-client[async]
```

Then import async client and create instance of this

```
from outline_vpn_api_client.async_client import AsyncOutlineClient

# Replace 'your.management.url' with your actual management URL
management_url = "your.management.url"

# Create an AsyncOutlineClient instance
client = AsyncOutlineClient(management_url=management_url)
```

### Console Version

The library also includes a command-line interface (CLI) for quick access. You can use the following command to interact with the server:

```bash
python3 -m outline_vpn_api_client management_url get_info
```

## AUTHOR

Created by **zeph1rr**  
Email: [grianton535@gmail.com](mailto:grianton535@gmail.com)