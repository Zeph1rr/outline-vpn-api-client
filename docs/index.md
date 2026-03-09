# outline-vpn-api-client

Welcome to the documentation for **outline-vpn-api-client** — a Python library for managing an Outline VPN server via the official Management API.

## Features

- Manage access keys: create, rename, delete, set data limits
- Configure server settings: hostname, port, default data limits
- Retrieve server metrics including per-key data transfer and detailed statistics
- Full async support via `AsyncOutlineClient`

## Installation

```bash
pip install outline-vpn-api-client
```

For async support:

```bash
pip install outline-vpn-api-client[async]
```

## Quick Start

```python
from outline_vpn_api_client import OutlineClient

client = OutlineClient(management_url="your.management.url")
print(client.get_information().model_dump())
```