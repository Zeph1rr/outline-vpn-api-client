import pytest
import json

from outline_vpn_api_client import OutlineClient, ResponseNotOkException

def test_acess_key_get_all(client: OutlineClient):
    data = client.access_keys.get_all()
    assert len(data) == 1
    assert data['accessKeys'][0]['id'] == '0'

@pytest.mark.parametrize('id, is_error', [(0, False), (10, True)])
def test_access_key_get(id: int, is_error: bool, client: OutlineClient):
    if is_error:
        with pytest.raises(ResponseNotOkException) as _ex:
            client.access_keys.get(id)
            assert 404 in _ex
    else:
        assert client.access_keys.get(id).get("id") == str(id)

@pytest.mark.parametrize('name, limit', [('first_test_client', None), ('second_test_client', 150000000000)])
def test_access_key_create(name: str, limit: int, client: OutlineClient):
    user = client.access_keys.create(name, limit=limit)
    assert user.get("name") == name
    if limit:
        assert user.get("dataLimit").get("bytes") == 150000000000

@pytest.mark.parametrize('id, name, limit, is_error', [(4, 'third_test_client', None, False), (3, 'fourth_test_client', 150000000000, False), (3, 'fourth_test_client', 150000000000, True)])
def test_access_key_create_with_special_id(id: int, name: str, limit: int, is_error: bool,  client: OutlineClient):
    if is_error:
        with pytest.raises(ResponseNotOkException) as _ex:
            client.access_keys.create_with_special_id(id, name, limit=limit)
            assert "Conflict" in _ex
    else:
        user = client.access_keys.create_with_special_id(id, name, limit=limit)
        assert user.get("id") == str(id)
        assert user.get("name") == name
        if limit:
            assert user.get("dataLimit").get("bytes") == 150000000000

def test_access_key_rename(client: OutlineClient):
    assert client.access_keys.rename(3, "renamed_fourth_test_client")
    assert client.access_keys.get(3).get("name") == "renamed_fourth_test_client"

def test_access_key_change_data_limit(client: OutlineClient):
    assert client.access_keys.change_data_limit(4, 150000000000)
    assert client.access_keys.get(4).get("dataLimit").get("bytes") == 150000000000

def test_access_key_remove_data_limit(client: OutlineClient):
    assert client.access_keys.remove_data_limit(4)
    assert client.access_keys.get(4).get("dataLimit") is None


def test_access_key_delete(client: OutlineClient):
    data = client.access_keys.get_all()
    for key in data['accessKeys']:
        assert client.access_keys.delete(key["id"])
        with pytest.raises(ResponseNotOkException) as _ex:
            client.access_keys.get(key["id"])
            assert 404 in _ex

def test_access_key_str_print(client: OutlineClient):
    assert json.loads(str(client.access_keys)) == client.access_keys.get_all()