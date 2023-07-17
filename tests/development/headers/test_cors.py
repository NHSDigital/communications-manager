import requests
import pytest
from lib import Assertions


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
TEST_METHODS = ["get", "post", "put", "delete"]


@pytest.mark.devtest
@pytest.mark.parametrize("method", METHODS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_cors_options(nhsd_apim_proxy_url, method, nhsd_apim_auth_headers):
    resp = requests.options(f"{nhsd_apim_proxy_url}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "*/*",
        "Origin": "https://my.website",
        "Access-Control-Request-Method": method
    })
    Assertions.assert_cors_response(resp, "https://my.website")


@pytest.mark.devtest
@pytest.mark.parametrize("method", TEST_METHODS)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_cors(nhsd_apim_proxy_url, method, nhsd_apim_auth_headers):
    resp = getattr(requests, method)(f"{nhsd_apim_proxy_url}", headers={
        **nhsd_apim_auth_headers,
        "Accept": "*/*",
        "Origin": "https://my.website"
    })

    Assertions.assert_cors_headers(resp, "https://my.website")