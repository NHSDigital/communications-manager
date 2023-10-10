import requests
import pytest
import uuid
from lib import Assertions, Permutations, Generators
from lib.constants import *

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
CORRELATION_IDS = [None, "e8bb49c6-06bc-44f7-8443-9244284640f8"]
INVALID_MESSAGE_VALUES = ["", [], 5, 0.1]
INVALID_NHS_NUMBER = ["999054860", "99905486090", "abcdefghij", "", [], {}, 5, 0.1]
INVALID_DOB = ["1990-10-1", "1990-1-10", "90-10-10", "10-12-1990", "1-MAY-2000", "1990/01/01", "", [], {}, 5, 0.1, None]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_invalid_body(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_body.rst
    """
    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id
        },
        data="{}SF{}NOTVALID",
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/"),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    MISSING_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_property_missing(nhsd_apim_proxy_url, property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_property_missing.rst
    """
    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=Permutations.new_dict_without_key(
            Generators.generate_valid_create_message_batch_body("sandbox"),
            property
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_missing_value_error(pointer),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    NULL_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_data_null(nhsd_apim_proxy_url, property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_data_null.rst
    """
    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=Permutations.new_dict_with_null_key(
            Generators.generate_valid_create_message_batch_body("sandbox"),
            property
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_null_value_error(pointer),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    INVALID_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_data_invalid(nhsd_apim_proxy_url, property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_data_invalid.rst
    """
    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_batch_body("sandbox"),
            property,
            "invalid string"
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error(pointer),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    DUPLICATE_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_data_duplicate(nhsd_apim_proxy_url, property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_data_duplicate.rst
    """
    # Add a duplicate message to the payload to trigger the duplicate error
    data = Generators.generate_valid_create_message_batch_body("sandbox")
    data["data"]["attributes"]["messages"].append(data["data"]["attributes"]["messages"][0])

    # Post the same message a 2nd time to trigger the duplicate error
    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=data,
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_duplicate_value_error(pointer),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    TOO_FEW_PROPERTIES_PATHS
)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_data_too_few_items(nhsd_apim_proxy_url, property, pointer, correlation_id):
    """
    .. include:: ../../partials/validation/test_data_too_few_items.rst
    """
    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=Permutations.new_dict_with_new_value(
            Generators.generate_valid_create_message_batch_body("sandbox"),
            property,
            []
        ),
    )

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_too_few_items_error(pointer),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("nhs_number", INVALID_NHS_NUMBER)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_invalid_nhs_number(nhsd_apim_proxy_url, nhs_number, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_nhs_number.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            **headers,
            "X-Correlation-Id": correlation_id
        }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    {
                        "messageReference": "72f2fa29-1570-47b7-9a67-63dc4b28fc1b",
                        "recipient": {
                            "nhsNumber": nhs_number,
                            "dateOfBirth": "2023-01-01"
                        },
                        "personalisation": {}
                    }
                ]
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_nhs_number_error("/data/attributes/messages/0/recipient/nhsNumber"),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("dob", INVALID_DOB)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_invalid_dob(nhsd_apim_proxy_url, dob, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_dob.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            **headers,
            "X-Correlation-Id": correlation_id
        }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    {
                        "messageReference": "72f2fa29-1570-47b7-9a67-63dc4b28fc1b",
                        "recipient": {
                            "nhsNumber": "9990548609",
                            "dateOfBirth": dob
                        },
                        "personalisation": {}
                    }
                ]
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/messages/0/recipient/dateOfBirth"),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_invalid_routing_plan(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_routing_plan.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            **headers,
            "X-Correlation-Id": correlation_id
        }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "invalid",
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    {
                        "messageReference": "72f2fa29-1570-47b7-9a67-63dc4b28fc1b",
                        "recipient": {
                            "nhsNumber": "9990548609",
                            "dateOfBirth": "2023-01-01"
                        },
                        "personalisation": {}
                    }
                ]
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/routingPlanId"),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_invalid_message_batch_reference(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_message_batch_reference.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            **headers,
            "X-Correlation-Id": correlation_id
        }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageBatchReference": "invalid",
                "messages": [
                    {
                        "messageReference": "72f2fa29-1570-47b7-9a67-63dc4b28fc1b",
                        "recipient": {
                            "nhsNumber": "9990548609",
                            "dateOfBirth": "2023-01-01"
                        },
                        "personalisation": {}
                    }
                ]
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/messageBatchReference"),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_invalid_message_reference(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/validation/test_invalid_message_reference.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            **headers,
            "X-Correlation-Id": correlation_id
        }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    {
                        "messageReference": "invalid",
                        "recipient": {
                            "nhsNumber": "9990548609",
                            "dateOfBirth": "2023-01-01"
                        },
                        "personalisation": {}
                    }
                ]
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/messages/0/messageReference"),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("invalid_value", INVALID_MESSAGE_VALUES)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_blank_value_under_messages(nhsd_apim_proxy_url, invalid_value, correlation_id):
    """
    .. include:: ../../partials/validation/test_blank_value_under_messages.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            **headers,
            "X-Correlation-Id": correlation_id
        }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    invalid_value
                ],
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_invalid_value_error("/data/attributes/messages/0"),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_null_value_under_messages(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/validation/test_null_value_under_messages.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/message-batches", headers={
            **headers,
            "X-Correlation-Id": correlation_id
        }, json={
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    None
                ],
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        400,
        Generators.generate_null_value_error("/data/attributes/messages/0"),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("number_of_errors", [99, 100, 101, 150, 200])
def test_validation_returns_at_max_errors(nhsd_apim_proxy_url, correlation_id, number_of_errors):
    """
    .. include:: ../../partials/validation/test_validation_returns_at_max_errors.rst
    """
    duplicate_message_reference = str(uuid.uuid4())
    data = {
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                "messageBatchReference": str(uuid.uuid1()),
                "messages": [
                    {
                        "messageReference": duplicate_message_reference,
                        "recipient": {
                            "nhsNumber": "9990548609",
                            "dateOfBirth": "2023-01-01"
                        },
                        "personalisation": {}
                    } for _ in range(number_of_errors)
                ],
            }
        }
    }
    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": correlation_id
        },
        json=data,
    )
    assert len(resp.json().get("errors")) <= NUM_MAX_ERRORS
