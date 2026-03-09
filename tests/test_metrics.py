import pytest
import json

from outline_vpn_api_client import OutlineClient

def test_metrics_check_enabled(client: OutlineClient):
    enabled = client.metrics.check_enabled()
    assert isinstance(enabled, bool)

@pytest.mark.parametrize("state", [True, False])
def test_metrics_change_enabled_state(state: bool, client: OutlineClient):
    assert client.metrics.change_enabled_state(state)
    assert client.metrics.check_enabled() == state

def test_metrics_get_data_transfer(client: OutlineClient):
    assert client.metrics.get_data_transfer().bytesTransferredByUserId is not None

def test_metrics_str_print(client: OutlineClient):
    assert json.loads(str(client.metrics)) == {"enabled": client.metrics.check_enabled()}