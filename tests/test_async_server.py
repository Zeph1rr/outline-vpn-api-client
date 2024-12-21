from os import getenv

import pytest
from outline_vpn_api_client import ResponseNotOkException
from outline_vpn_api_client.async_client import AsyncOutlineClient


async def test_async_server_get_info(async_client: AsyncOutlineClient):
    info = await async_client.server.get_information()
    assert info.get("serverId") == getenv("OUTLINE_SERVER_ID")

async def test_async_server_change_hostname(async_client: AsyncOutlineClient):
    hostname = getenv("OUTLINE_URL").split('//')[1].split(':')[0]
    assert await async_client.server.change_hostname(hostname)
    info = await async_client.server.get_information()
    assert info.get("hostnameForAccessKeys") == hostname

async def test_async_server_rename(async_client: AsyncOutlineClient):
    assert await async_client.server.rename("Renamed server")
    info = await async_client.server.get_information()
    assert info.get("name") == "Renamed server"

@pytest.mark.parametrize("port", [12345, -1])
async def test_async_server_change_port(port: int, async_client: AsyncOutlineClient):
    if port == -1:
        port = int(getenv("OUTLINE_DEFAULT_PORT"))
    assert await async_client.server.change_default_port_for_new_keys(port)
    info = await async_client.server.get_information()
    assert info.get("portForNewAccessKeys") == port

@pytest.mark.parametrize('limit,is_error', [(150*10**9, False), (-12, True)])
async def test_async_server_set_default_data_limit(limit: int, is_error: bool, async_client: AsyncOutlineClient):
    if is_error:
        with pytest.raises(ResponseNotOkException) as _ex:
            await async_client.server.set_server_default_limits(limit)
            assert "non-negative" in str(_ex.value)
    else:
        assert await async_client.server.set_server_default_limits(limit)
        info = await async_client.server.get_information()
        assert info.get("accessKeyDataLimit").get("bytes") == limit

async def test_async_server_remove_default_data_limit(async_client: AsyncOutlineClient):
    assert await async_client.server.remove_server_default_limits()
    info = await async_client.server.get_information()
    assert info.get("accessKeyDataLimit") is None
