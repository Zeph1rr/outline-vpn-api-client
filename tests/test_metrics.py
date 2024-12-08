import pytest

from outline_vpn_api_client import OutlineClient

def test_metrics_check_enabled(client: OutlineClient):
    assert not client.metrics.check_enabled()

@pytest.mark.parametrize("state", [True, False])
def test_metrics_change_enabled_state(state: bool, client: OutlineClient):
    assert client.metrics.change_enabled_state(state)
    assert client.metrics.check_enabled() == state

def test_metrics_get_data_transfer(client: OutlineClient):
    assert client.metrics.get_data_transfer().get("bytesTransferredByUserId") is not None