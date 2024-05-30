import requests
import pytest
from lib import Assertions, Generators, Authentication
from lib.constants.messages_paths import MESSAGES_ENDPOINT


@pytest.mark.devtest
def test_message_id_not_belonging_to_client_id(nhsd_apim_proxy_url):
    """
    .. include:: ../../partials/not_found/test_message_id_not_belonging_to_client_id.rst
    """
    resp = requests.get(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}/successful_email_other_owner",
        headers={"Authorization": Authentication.generate_authentication("internal-dev")}
    )
    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_not_found_error(),
        None
    )


@pytest.mark.devtest
def test_message_id_that_does_not_exist(nhsd_apim_proxy_url):
    """
    .. include:: ../../partials/not_found/test_message_id_that_does_not_exist.rst
    """
    resp = requests.get(
        f"{nhsd_apim_proxy_url}{MESSAGES_ENDPOINT}/does_not_exist",
        headers={"Authorization": Authentication.generate_authentication("internal-dev")}
    )
    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_not_found_error(),
        None
    )
