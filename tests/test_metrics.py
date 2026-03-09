import pytest
import json
from datetime import datetime, timezone, timedelta

from outline_vpn_api_client import OutlineClient

def test_metrics_check_enabled(client: OutlineClient):
    assert not client.metrics.check_enabled()

@pytest.mark.parametrize("state", [True, False])
def test_metrics_change_enabled_state(state: bool, client: OutlineClient):
    assert client.metrics.change_enabled_state(state)
    assert client.metrics.check_enabled() == state

def test_metrics_get_data_transfer(client: OutlineClient):
    assert client.metrics.get_data_transfer().bytesTransferredByUserId is not None

def test_metrics_str_print(client: OutlineClient):
    assert json.loads(str(client.metrics)) == {"enabled": client.metrics.check_enabled()}

def test_metrics_get_server_metrics_returns_data(client: OutlineClient):
    since = datetime.now(timezone.utc) - timedelta(days=30)
    result = client.metrics.get_server_metrics(since)
    assert result.server is not None
    assert isinstance(result.accessKeys, list)

def test_metrics_get_server_metrics_server_fields(client: OutlineClient):
    since = datetime.now(timezone.utc) - timedelta(days=30)
    result = client.metrics.get_server_metrics(since)
    server = result.server
    if server.dataTransferred is not None:
        assert server.dataTransferred.bytes >= 0
    if server.tunnelTime is not None:
        assert server.tunnelTime.seconds >= 0

def test_metrics_get_server_metrics_access_key_fields(client: OutlineClient):
    since = datetime.now(timezone.utc) - timedelta(days=30)
    result = client.metrics.get_server_metrics(since)
    for key in result.accessKeys:
        assert isinstance(key.accessKeyId, int)
        if key.dataTransferred is not None:
            assert key.dataTransferred.bytes >= 0
        if key.tunnelTime is not None:
            assert key.tunnelTime.seconds >= 0

def test_metrics_get_server_metrics_future_since(client: OutlineClient):
    since = datetime.now(timezone.utc) + timedelta(days=1)
    result = client.metrics.get_server_metrics(since)
    assert result.server is not None
    assert isinstance(result.accessKeys, list)