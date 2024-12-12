import warnings
import os

import pytest

from outline_vpn_api_client import OutlineClient
from .utils import *

@pytest.fixture(scope="session", autouse=True)
def prepare_server():
    output = run_server()
    api_url = find_api_url(output)
    set_environment(api_url)
    print(os.environ)
    yield
    stop_server()

@pytest.fixture()
def client() -> OutlineClient:
    warnings.filterwarnings("ignore")
    client = OutlineClient(os.getenv("OUTLINE_URL"))
    return client