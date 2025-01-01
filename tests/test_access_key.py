import pytest
import json

from outline_vpn_api_client import OutlineClient, ResponseNotOkException

def test_acess_key_get_all(client: OutlineClient):
    data = client.access_keys.get_all()
    assert len(data) == 1
    assert data.accessKeys[0].id == '0'

@pytest.mark.parametrize('id, is_error', [(0, False), (10, True)])
def test_access_key_get(id: int, is_error: bool, client: OutlineClient):
    if is_error:
        with pytest.raises(ResponseNotOkException) as _ex:
            client.access_keys.get(id)
            assert 404 in _ex
    else:
        assert client.access_keys.get(id).id == str(id)

@pytest.mark.parametrize('name, limit', [('first_test_client', None), ('second_test_client', 150000000000)])
def test_access_key_create(name: str, limit: int, client: OutlineClient):
    user = client.access_keys.create(name, limit=limit)
    assert user.name == name
    if limit:
        assert user.dataLimit.bytes == 150000000000

@pytest.mark.parametrize('id, name, limit, is_error', [(212, 'third_test_client', None, False), (415, 'fourth_test_client', 150000000000, False), (415, 'fourth_test_client', 150000000000, True)])
def test_access_key_create_with_special_id(id: int, name: str, limit: int, is_error: bool,  client: OutlineClient):
    if is_error:
        with pytest.raises(ResponseNotOkException) as _ex:
            client.access_keys.create_with_special_id(id, name, limit=limit)
            assert "Conflict" in _ex
    else:
        user = client.access_keys.create_with_special_id(id, name, limit=limit)
        assert user.id == str(id)
        assert user.name == name
        if limit:
            assert user.dataLimit.bytes == 150000000000

def test_access_key_rename(client: OutlineClient):
    assert client.access_keys.rename(415, "renamed_fourth_test_client")
    assert client.access_keys.get(415).name == "renamed_fourth_test_client"

def test_access_key_change_data_limit(client: OutlineClient):
    assert client.access_keys.change_data_limit(212, 150000000000)
    assert client.access_keys.get(212).dataLimit.bytes == 150000000000

def test_access_key_remove_data_limit(client: OutlineClient):
    assert client.access_keys.remove_data_limit(212)
    assert client.access_keys.get(212).dataLimit is None


def test_access_key_delete(client: OutlineClient):
    data = client.access_keys.get_all()
    for key in data.accessKeys:
        if int(key.id) != 0: 
            assert client.access_keys.delete(key.id)
            with pytest.raises(ResponseNotOkException) as _ex:
                client.access_keys.get(key.id)
                assert 404 in _ex

def test_access_key_str_print(client: OutlineClient):
    assert json.loads(str(client.access_keys)) == client.access_keys.get_all().model_dump()