import requests
import pytest
import uuid
from lib import Assertions, Generators
from lib.constants import NUM_MAX_ERRORS

NUM_MESSAGES = 50000


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_create_messages_large_valid_payload(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    data = Generators.generate_valid_create_message_batch_body(True)

    # around 50k messages gives us close to our max body size
    data["data"]["attributes"]["messages"] = []
    for i in range(0, NUM_MESSAGES):
        data["data"]["attributes"]["messages"].append({
            "messageReference": str(uuid.uuid1()),
            "recipient": {
                "nhsNumber": "1234567890"
            },
            "personalisation": {}
        })

    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
        **nhsd_apim_auth_headers,
        "Accept": "application/json",
        "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_201_response(resp, data["data"]["attributes"]["messageBatchReference"])


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_create_messages_large_invalid_payload(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    data = Generators.generate_valid_create_message_batch_body(True)

    # around 50k messages gives us close to our max body size
    data["data"]["attributes"]["messages"] = []
    for i in range(0, NUM_MESSAGES):
        data["data"]["attributes"]["messages"].append({
            "messageReference": str(uuid.uuid1()),
            "recipient": {
                "nhsNumber": "not valid",
            },
            "personalisation": {}
        })

    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
        **nhsd_apim_auth_headers,
        "Accept": "application/json",
        "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_error_with_optional_correlation_id(resp, 400, None, None)
    assert len(resp.json().get("errors")) == NUM_MAX_ERRORS


@pytest.mark.devtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_create_messages_large_not_unique_payload(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    data = Generators.generate_valid_create_message_batch_body(True)

    # around 50k messages gives us close to our max body size
    data["data"]["attributes"]["messages"] = []
    reference = str(uuid.uuid1())
    for i in range(0, NUM_MESSAGES):
        data["data"]["attributes"]["messages"].append({
            "messageReference": reference,
            "recipient": {
                "nhsNumber": "not valid",
            },
            "personalisation": {}
        })

    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
        **nhsd_apim_auth_headers,
        "Accept": "application/json",
        "Content-Type": "application/json"
        }, json=data
    )
    Assertions.assert_error_with_optional_correlation_id(resp, 400, None, None)
    assert len(resp.json().get("errors")) == NUM_MAX_ERRORS
