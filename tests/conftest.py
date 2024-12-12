import warnings
import os

import pytest

from outline_vpn_api_client import OutlineClient

@pytest.fixture(scope="session", autouse=True)
def set_environment():
    api_url = os.getenv("API_URL")
    client = OutlineClient(api_url)
    info = client.server.get_information()
    os.environ["OUTLINE_URL"] = api_url
    os.environ["OUTLINE_SERVER_ID"] = info['serverId']
    os.environ["OUTLINE_DEFAULT_PORT"] = str(info['portForNewAccessKeys'])

@pytest.fixture()
def client() -> OutlineClient:
    warnings.filterwarnings("ignore")
    client = OutlineClient(os.getenv("OUTLINE_URL"))
    return client