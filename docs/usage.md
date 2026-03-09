# Usage

## Initializing the Client

```python
from outline_vpn_api_client import OutlineClient

client = OutlineClient(management_url="your.management.url")
```

> **Note:** By default, SSL certificate verification is disabled (`ssl_verify=False`). This is intentional,
> as Outline servers typically use self-signed certificates. You can enable verification by passing
> `ssl_verify=True` if your server has a valid certificate.

---

## Server

### Get server information

```python
info = client.server.get_information()
print(info.serverId)
print(info.name)
```

### Rename the server

```python
client.server.rename("My VPN Server")
```

### Change hostname

```python
client.server.change_hostname("vpn.example.com")
```

### Change default port for new access keys

```python
client.server.change_default_port_for_new_keys(12345)
```

### Set a default data limit for all access keys

```python
client.server.set_server_default_limits(10 ** 9)  # 1 GB
```

### Remove the default data limit

```python
client.server.remove_server_default_limits()
```

---

## Access Keys

### List all access keys

```python
keys = client.access_keys.get_all()
for key in keys.accessKeys:
    print(key.id, key.name)
```

### Get a specific access key

```python
key = client.access_keys.get(0)
print(key.accessUrl)
```

### Create an access key

```python
# Minimal
key = client.access_keys.create(name="Alice")

# With data limit (bytes)
key = client.access_keys.create(name="Bob", limit=10 ** 9)

# With custom password and port
key = client.access_keys.create(name="Charlie", password="MyPass123", port=12345)
```

### Create an access key with a specific ID

```python
key = client.access_keys.create_with_special_id(
    id=42,
    name="Dave",
    password="MyPass123",
    port=12345,
    limit=10 ** 9,
)
```

### Rename an access key

```python
client.access_keys.rename(42, "Dave Renamed")
```

### Set a data limit on an access key

```python
client.access_keys.change_data_limit(42, 5 * 10 ** 9)  # 5 GB
```

### Remove a data limit from an access key

```python
client.access_keys.remove_data_limit(42)
```

### Delete an access key

```python
client.access_keys.delete(42)
```

---

## Metrics

### Check if metrics sharing is enabled

```python
print(client.metrics.check_enabled())
```

### Enable or disable metrics sharing

```python
client.metrics.change_enabled_state(True)   # enable
client.metrics.change_enabled_state(False)  # disable
```

### Get data transfer per access key

```python
transfer = client.metrics.get_data_transfer()
for key_id, bytes_used in transfer.bytesTransferredByUserId.items():
    print(f"Key {key_id}: {bytes_used / 10**6:.1f} MB")
```

### Get detailed server metrics (experimental)

```python
from datetime import datetime, timezone, timedelta

metrics = client.metrics.get_server_metrics(
    since=datetime.now(timezone.utc) - timedelta(days=30)
)

print(metrics.server.dataTransferred.bytes)
print(metrics.server.bandwidth.peak.data.bytes)

for key in metrics.accessKeys:
    bytes_used = key.dataTransferred.bytes if key.dataTransferred else 0
    print(f"Key {key.accessKeyId}: {bytes_used / 10**6:.1f} MB")
```

> **Note:** This endpoint is experimental and may change in future versions of the Outline server.

---

## Async Usage

Install the async version of the package:

```bash
pip install outline-vpn-api-client[async]
```

All methods are identical to the sync client but must be awaited:

```python
import asyncio
from datetime import datetime, timezone, timedelta
from outline_vpn_api_client.async_client import AsyncOutlineClient

client = AsyncOutlineClient(management_url="your.management.url")

async def main():
    # Server info
    info = await client.server.get_information()
    print(info.serverId)

    # Create a key
    key = await client.access_keys.create(name="Alice", limit=10 ** 9)
    print(key.accessUrl)

    # Detailed metrics
    metrics = await client.metrics.get_server_metrics(
        since=datetime.now(timezone.utc) - timedelta(days=30)
    )
    print(metrics.server.dataTransferred.bytes)

asyncio.run(main())
```

---

## Error Handling

All methods raise `ResponseNotOkException` on server-side errors:

```python
from outline_vpn_api_client import OutlineClient, ResponseNotOkException

client = OutlineClient(management_url="your.management.url")

try:
    key = client.access_keys.get(999)
except ResponseNotOkException as e:
    print(e)
    # An error occurred: 404 - {'code': 'NotFound', 'message': 'Access key "999" not found'}
```