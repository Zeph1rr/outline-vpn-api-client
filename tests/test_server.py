import json
from os import getenv

import pytest

from outline_vpn_api_client import OutlineClient, ResponseNotOkException


def test_server_get_info(client: OutlineClient):
    info = client.server.get_information()
    assert info.get("serverId") == getenv("OUTLINE_SERVER_ID")

def test_server_change_hostname(client: OutlineClient):
    hostname = getenv("OUTLINE_URL").split('//')[1].split(':')[0]
    assert client.server.change_hostname(hostname)
    assert client.server.get_information().get("hostnameForAccessKeys") == hostname

def test_server_rename(client: OutlineClient):
    assert client.server.rename("Renamed server")
    assert client.server.get_information().get("name") == "Renamed server"

@pytest.mark.parametrize("port", [12345, -1])
def test_server_change_port(port: int, client: OutlineClient):
    if port == -1:
        port = int(getenv("OUTLINE_DEFAULT_PORT"))
    assert client.server.change_default_port_for_new_keys(port)
    assert client.server.get_information().get("portForNewAccessKeys") == port

@pytest.mark.parametrize('limit,is_error', [(150*10**9, False), (-12, True)])
def test_server_set_default_data_limit(limit: int, is_error: bool, client: OutlineClient):
    if is_error:
        with pytest.raises(ResponseNotOkException) as _ex:
            client.server.set_server_default_limits(limit)
            assert "non-negative" in _ex
    else:
        assert client.server.set_server_default_limits(limit)
        assert client.server.get_information().get("accessKeyDataLimit").get("bytes") == limit

def test_server_remove_default_data_limit(client: OutlineClient):
    assert client.server.remove_server_default_limits()
    assert client.server.get_information().get("accessKeyDataLimit") is None

def test_server_str_print(client: OutlineClient):
    assert json.loads(str(client.server)) == client.server.get_information()