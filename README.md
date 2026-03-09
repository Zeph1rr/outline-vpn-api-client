# OUTLINE-VPN-API-CLIENT

[![PyPI - Version](https://img.shields.io/pypi/v/outline-vpn-api-client?style=plastic)](https://pypi.org/project/outline-vpn-api-client/)
![PyPI - Format](https://img.shields.io/pypi/format/outline-vpn-api-client?style=plastic)
![GitHub Release](https://img.shields.io/github/v/release/Zeph1rr/outline-vpn-api-client?style=plastic)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Zeph1rr/outline-vpn-api-client/tests.yml?style=plastic&label=tests)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/outline-vpn-api-client?style=plastic)
![GitHub License](https://img.shields.io/github/license/zeph1rr/outline-vpn-api-client?style=plastic)
[![Documentation Status](https://readthedocs.org/projects/outline-vpn-api-client/badge/?version=latest&style=plastic)](https://outline-vpn-api-client.readthedocs.io/en/latest/)


## DESCRIPTION

Python client for the [Outline VPN Management API](https://github.com/OutlineFoundation/outline-server). Manage access keys, configure server settings, and retrieve metrics — both synchronously and asynchronously.

## INSTALLATION

```bash
pip install outline-vpn-api-client
```

For async support:

```bash
pip install outline-vpn-api-client[async]
```

## QUICK START

```python
from outline_vpn_api_client import OutlineClient

client = OutlineClient(management_url="your.management.url")

# Get server info
print(client.get_information().model_dump())

# Create an access key
key = client.access_keys.create(name="Alice", limit=10**9)
print(key.accessUrl)
```

For full usage examples and API reference, see the [documentation](https://outline-vpn-api-client.readthedocs.io/en/latest/).

## HANDLING ERRORS

```python
from outline_vpn_api_client import OutlineClient, ResponseNotOkException

try:
    client.access_keys.get(999)
except ResponseNotOkException as e:
    print(e)
```

## AUTHOR

Created by **zeph1rr**  
Email: [grianton535@gmail.com](mailto:grianton535@gmail.com)