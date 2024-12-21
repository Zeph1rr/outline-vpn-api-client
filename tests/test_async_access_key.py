import pytest
import json

from outline_vpn_api_client import ResponseNotOkException
from outline_vpn_api_client.async_client import AsyncOutlineClient

async def test_acess_key_get_all(async_client: AsyncOutlineClient):
    data = await async_client.access_keys.get_all()
    assert len(data) == 1
    assert data['accessKeys'][0]['id'] == '0'

@pytest.mark.parametrize('id, is_error', [(0, False), (10, True)])
async def test_access_key_get(id: int, is_error: bool, async_client: AsyncOutlineClient):
    if is_error:
        with pytest.raises(ResponseNotOkException) as _ex:
            await async_client.access_keys.get(id)
            assert 404 in _ex
    else:
        data = await async_client.access_keys.get(id)
        assert data.get("id") == str(id)

@pytest.mark.parametrize('name, limit', [('first_test_client', None), ('second_test_client', 150000000000)])
async def test_access_key_create(name: str, limit: int, async_client: AsyncOutlineClient):
    user = await async_client.access_keys.create(name, limit=limit)
    assert user.get("name") == name
    if limit:
        assert user.get("dataLimit").get("bytes") == 150000000000

@pytest.mark.parametrize('id, name, limit, is_error', [(212, 'third_test_client', None, False), (415, 'fourth_test_client', 150000000000, False), (415, 'fourth_test_client', 150000000000, True)])
async def test_access_key_create_with_special_id(id: int, name: str, limit: int, is_error: bool,  async_client: AsyncOutlineClient):
    if is_error:
        with pytest.raises(ResponseNotOkException) as _ex:
            await async_client.access_keys.create_with_special_id(id, name, limit=limit)
            assert "Conflict" in _ex
    else:
        user = await async_client.access_keys.create_with_special_id(id, name, limit=limit)
        assert user.get("id") == str(id)
        assert user.get("name") == name
        if limit:
            assert user.get("dataLimit").get("bytes") == 150000000000

async def test_access_key_rename(async_client: AsyncOutlineClient):
    assert await async_client.access_keys.rename(415, "renamed_fourth_test_client")
    data = await async_client.access_keys.get(415)
    assert data.get("name") == "renamed_fourth_test_client"

async def test_access_key_change_data_limit(async_client: AsyncOutlineClient):
    assert await async_client.access_keys.change_data_limit(212, 150000000000)
    data = await async_client.access_keys.get(212)
    assert data.get("dataLimit").get("bytes") == 150000000000

async def test_access_key_remove_data_limit(async_client: AsyncOutlineClient):
    assert await async_client.access_keys.remove_data_limit(212)
    data = await async_client.access_keys.get(212)
    assert data.get("dataLimit") is None


async def test_access_key_delete(async_client: AsyncOutlineClient):
    data = await async_client.access_keys.get_all()
    for key in data['accessKeys']:
        if int(key["id"]) != 0: 
            assert await async_client.access_keys.delete(key["id"])
            with pytest.raises(ResponseNotOkException) as _ex:
                await async_client.access_keys.get(key["id"])
                assert 404 in _ex