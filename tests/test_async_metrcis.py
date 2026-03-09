import pytest
from datetime import datetime, timezone, timedelta

from outline_vpn_api_client.async_client import AsyncOutlineClient

async def test_async_metrics_check_enabled(async_client: AsyncOutlineClient):
    enabled = await async_client.metrics.check_enabled()
    assert isinstance(enabled, bool)

@pytest.mark.parametrize("state", [True, False])
async def test_async_metrics_change_enabled_state(state: bool, async_client: AsyncOutlineClient):
    assert await async_client.metrics.change_enabled_state(state)
    assert await async_client.metrics.check_enabled() == state

async def test_async_metrics_get_data_transfer(async_client: AsyncOutlineClient):
    response = await async_client.metrics.get_data_transfer()
    assert response.bytesTransferredByUserId is not None

async def test_async_metrics_get_server_metrics_returns_data(async_client: AsyncOutlineClient):
    since = datetime.now(timezone.utc) - timedelta(days=30)
    result = await async_client.metrics.get_server_metrics(since)
    assert result.server is not None
    assert isinstance(result.accessKeys, list)

async def test_async_metrics_get_server_metrics_server_fields(async_client: AsyncOutlineClient):
    since = datetime.now(timezone.utc) - timedelta(days=30)
    result = await async_client.metrics.get_server_metrics(since)
    server = result.server
    if server.dataTransferred is not None:
        assert server.dataTransferred.bytes >= 0
    if server.tunnelTime is not None:
        assert server.tunnelTime.seconds >= 0

async def test_async_metrics_get_server_metrics_access_key_fields(async_client: AsyncOutlineClient):
    since = datetime.now(timezone.utc) - timedelta(days=30)
    result = await async_client.metrics.get_server_metrics(since)
    for key in result.accessKeys:
        assert isinstance(key.accessKeyId, int)
        if key.dataTransferred is not None:
            assert key.dataTransferred.bytes >= 0
        if key.tunnelTime is not None:
            assert key.tunnelTime.seconds >= 0
