# AsyncMetrics

::: outline_vpn_api_client.async_client.AsyncMetrics

## Note on `get_server_metrics`

The `get_server_metrics` method uses the `GET /experimental/server/metrics` endpoint,
which is **experimental** and may be unstable or unavailable depending on your Outline
server version.

**Requirements:**

- Metrics sharing must be enabled: `await client.metrics.change_enabled_state(True)`
- The endpoint behavior and response format may change without notice in future server releases