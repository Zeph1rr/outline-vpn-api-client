# Metrics

::: outline_vpn_api_client.client.Metrics

## Note on `get_server_metrics`

The `get_server_metrics` method uses the `GET /experimental/server/metrics` endpoint,
which is **experimental** and may be unstable or unavailable depending on your Outline
server version.

**Requirements:**

- Metrics sharing must be enabled: `client.metrics.change_enabled_state(True)`
- The endpoint behavior and response format may change without notice in future server releases