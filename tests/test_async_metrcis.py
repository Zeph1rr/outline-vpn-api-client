import pytest

from outline_vpn_api_client.async_client import AsyncOutlineClient

async def test_async_metrics_check_enabled(async_client: AsyncOutlineClient):
    assert not await async_client.metrics.check_enabled()

@pytest.mark.parametrize("state", [True, False])
async def test_async_metrics_change_enabled_state(state: bool, async_client: AsyncOutlineClient):
    assert await async_client.metrics.change_enabled_state(state)
    assert await async_client.metrics.check_enabled() == state

async def test_async_metrics_get_data_transfer(async_client: AsyncOutlineClient):
    response = await async_client.metrics.get_data_transfer()
    assert response.get("bytesTransferredByUserId") is not None