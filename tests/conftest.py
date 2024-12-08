import warnings
from os import getenv

import pytest

from outline_vpn_api_client import OutlineClient

@pytest.fixture()
def client() -> OutlineClient:
    warnings.filterwarnings("ignore")
    client = OutlineClient(getenv("OUTLINE_URL"))
    return client