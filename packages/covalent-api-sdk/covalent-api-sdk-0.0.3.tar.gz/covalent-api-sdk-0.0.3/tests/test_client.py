import pytest
from covalent import Client

class TestClient:
    """ security service testing class """

    @pytest.fixture
    def client(self):
        """ initialize client """
        return Client("bad_key")

    def test_client_key_fail(self, client: Client):
        """ test for bad client key to access approvals endpoint fail """
        fail_appr = client.security_service.get_approvals("eth-mainnet", "demo.eth")
        assert fail_appr.error is True