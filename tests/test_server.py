import json
from os import getenv

import pytest

from outline_vpn_api_client import OutlineClient


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

@pytest.mark.parametrize("port", [12345, int(getenv("OUTLINE_DEFAULT_PORT"))])
def test_server_change_port(port: int, client: OutlineClient):
    assert client.server.change_default_port_for_new_keys(port)
    assert client.server.get_information().get("portForNewAccessKeys") == port

def test_server_set_default_data_limit(client: OutlineClient):
    assert client.server.set_server_default_limits(150000000000)
    assert client.server.get_information().get("accessKeyDataLimit").get("bytes") == 150000000000

def test_server_remove_default_data_limit(client: OutlineClient):
    assert client.server.remove_server_default_limits()
    assert client.server.get_information().get("accessKeyDataLimit") is None

def test_server_str_print(client: OutlineClient):
    assert json.loads(str(client.server)) == client.server.get_information()