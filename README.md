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

> **Note:** By default, SSL certificate verification is disabled (`ssl_verify=False`). This is intentional, as Outline servers typically use self-signed certificates. You can enable verification by passing `ssl_verify=True` if your server has a valid certificate.

### Retrieving Server Information

```python
import json

# Fetch server information and pretty-print it
print(json.dumps(client.get_information().model_dump(), ensure_ascii=False, indent=4))
```

### Creating Access Keys

#### Creating a Key Without Limits

```python
client.access_keys.create(name="Example Key")
```

#### Creating a Key With a Data Limit

```python
# Replace 'limit' with the desired data limit in bytes
client.access_keys.create(name="Example Key with Limit", limit=10**9)  # Example: 1 GB limit
```

#### Creating a Key With a Custom Password and Port

```python
client.access_keys.create(
    name="Example Key",
    password="MyCustomPassword",
    port=12345,
)
```

#### Creating a Key With a Specific ID

```python
client.access_keys.create_with_special_id(
    id=42,
    name="Example Key",
    password="MyCustomPassword",
    port=12345,
    limit=10**9,
)
```

### Retrieving Server Metrics

#### Basic Metrics (data transferred per key)

```python
transfer = client.metrics.get_data_transfer()
print(transfer.bytesTransferredByUserId)
```

#### Detailed Server Metrics (experimental)

```python
from datetime import datetime, timezone, timedelta

# Get metrics for the last 30 days
metrics = client.metrics.get_server_metrics(
    since=datetime.now(timezone.utc) - timedelta(days=30)
)

print(metrics.server.dataTransferred.bytes)
print(metrics.server.bandwidth.peak.data.bytes)

for key in metrics.accessKeys:
    print(key.accessKeyId, key.dataTransferred.bytes if key.dataTransferred else 0)
```

> **Note:** This endpoint is experimental and may change in future versions of the Outline server.

### Handling Errors

The library uses a custom exception, `ResponseNotOkException`, to handle server-side errors. This exception is raised whenever the API returns an unexpected response.

```python
from outline_vpn_api_client import ResponseNotOkException

try:
    info = client.get_information()
    print(info)
except ResponseNotOkException as e:
    print(e)
```

The error message provides details about the HTTP status code and the error message returned by the API:

```
outline_vpn_api_client.client.ResponseNotOkException: An error occurred: 404 - {'code': 'NotFound', 'message': 'Access key "100" not found'}
```

### Async Usage

For async usage, install the async version of the package:

```
pip install outline-vpn-api-client[async]
```

Then import the async client and create an instance:

```python
from outline_vpn_api_client.async_client import AsyncOutlineClient

management_url = "your.management.url"

client = AsyncOutlineClient(management_url=management_url)
```

All methods are identical to the sync client, but must be awaited:

```python
import asyncio
from datetime import datetime, timezone, timedelta

async def main():
    info = await client.get_information()
    print(info.model_dump())

    metrics = await client.metrics.get_server_metrics(
        since=datetime.now(timezone.utc) - timedelta(days=30)
    )
    print(metrics.server.dataTransferred.bytes)

asyncio.run(main())
```

### Console Version

The library also includes a command-line interface (CLI) for quick access:

```bash
python3 -m outline_vpn_api_client management_url get_info
```

## AUTHOR

Created by **zeph1rr**  
Email: [grianton535@gmail.com](mailto:grianton535@gmail.com)