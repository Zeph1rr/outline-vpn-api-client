import warnings
import os

import pytest

from outline_vpn_api_client import OutlineClient
from .utils import *

@pytest.fixture(scope="session", autouse=True)
def run_server():
    output = do_ssh_request(os.getenv("SSH_HOST"), "/home/zeph1rr/outline_test/start_server.sh")
    api_url = find_api_url(output)
    set_environment(api_url)
    print(os.environ)
    yield
    do_ssh_request(os.getenv("SSH_HOST"), "/home/zeph1rr/outline_test/stop_server.sh")

@pytest.fixture()
def client() -> OutlineClient:
    warnings.filterwarnings("ignore")
    client = OutlineClient(os.getenv("OUTLINE_URL"))
    return client