import warnings
import os

import pytest

from outline_vpn_api_client import OutlineClient
from outline_vpn_api_client.async_client import AsyncOutlineClient

@pytest.fixture(scope="session", autouse=True)
def set_environment():
    api_url = os.getenv("API_URL")
    if not api_url:
        raise ValueError("API_URL environment variable is not set.")
    
    client = OutlineClient(api_url)
    info = client.server.get_information()
    os.environ["OUTLINE_URL"] = api_url
    os.environ["OUTLINE_SERVER_ID"] = info.serverId
    os.environ["OUTLINE_DEFAULT_PORT"] = str(info.portForNewAccessKeys)

@pytest.fixture()
def client() -> OutlineClient:
    warnings.filterwarnings("ignore")
    return OutlineClient(os.getenv("OUTLINE_URL"))

@pytest.fixture()
async def async_client() -> AsyncOutlineClient:
    """
    Provide an asynchronous Outline client instance for tests.
    """
    warnings.filterwarnings("ignore")
    return AsyncOutlineClient(os.getenv("OUTLINE_URL"))