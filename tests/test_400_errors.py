import requests
import pytest
import uuid

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
full_data = {
  "data": {
    "type": "MessageBatch",
    "attributes": {
      "routingPlanId": "2fd7f5c4-802e-4092-bd3d-276bb199df62",
      "messageBatchReference": "da0b1495-c7cb-468c-9d81-07dee089d728",
      "messages": [
        {
          "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
          "recipient": {
            "nhsNumber": "1234567890",
            "dateOfBirth": "1982-03-17"
          },
          "personalisation": {}
        }
      ]
    }
  }
}
x_correlation_id_value = f"0{str(uuid.uuid4())[1:]}"


"""
Invalid body 400 tests
"""


@pytest.mark.sandboxtest
def test_invalid_body_sandbox(nhsd_apim_proxy_url):
    expected_error = {
        "id": "CM_INVALID_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Invalid value",
        "detail": "The property at the specified location does not allow this value.",
        "source": {
            "pointer": "/"
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers=headers,
        data="{}SF{}NOTVALID",
    )

    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")


@pytest.mark.sandboxtest
def test_invalid_body_sandbox_with_correlation_id(nhsd_apim_proxy_url):
    expected_error = {
        "id": "CM_INVALID_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Invalid value",
        "detail": "The property at the specified location does not allow this value.",
        "source": {
            "pointer": "/"
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": x_correlation_id_value},
        data="{}SF{}NOTVALID",
    )

    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")
    assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_invalid_body_prod(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    expected_error = {
        "id": "CM_INVALID_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Invalid value",
        "detail": "The property at the specified location does not allow this value.",
        "source": {
            "pointer": "/"
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={**nhsd_apim_auth_headers, **headers},
        data="{}SF{}NOTVALID",
    )

    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")


@pytest.mark.prodtest
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_invalid_body_prod_with_correlation_id(nhsd_apim_proxy_url, nhsd_apim_auth_headers):
    expected_error = {
        "id": "CM_INVALID_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Invalid value",
        "detail": "The property at the specified location does not allow this value.",
        "source": {
            "pointer": "/"
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **nhsd_apim_auth_headers,
            **headers,
            "X-Correlation-Id": x_correlation_id_value},
        data="{}SF{}NOTVALID",
    )

    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")
    assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value


"""
Missing property 400 test
"""

_missing_properties = [
    ("data", "/data"),
    ("type", "/data/type"),
    ("attributes", "/data/attributes"),
    ("routingPlanId", "/data/attributes/routingPlanId"),
    ("messageBatchReference", "/data/attributes/messageBatchReference"),
    ("messages", "/data/attributes/messages"),
    ("messageReference", "/data/attributes/messages/0/messageReference"),
    ("recipient", "/data/attributes/messages/0/recipient"),
    ("nhsNumber", "/data/attributes/messages/0/recipient/nhsNumber"),
]


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    _missing_properties
)
def test_property_missing_sandbox(nhsd_apim_proxy_url, property, pointer):
    data = new_dict_without_key(full_data, property)

    expected_error = {
        "id": "CM_MISSING_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Missing property",
        "detail": "The property at the specified location is required, but was not present in the request.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers=headers,
        json=data,
    )

    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    _missing_properties
)
def test_property_missing_sandbox_with_correlation_id(nhsd_apim_proxy_url, property, pointer):
    data = new_dict_without_key(full_data, property)

    expected_error = {
        "id": "CM_MISSING_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Missing property",
        "detail": "The property at the specified location is required, but was not present in the request.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": x_correlation_id_value
        },
        json=data,
    )

    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")
    assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value


@pytest.mark.prodtest
@pytest.mark.parametrize(
    "property, pointer",
    _missing_properties
)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_property_missing_prod(nhsd_apim_proxy_url, nhsd_apim_auth_headers, property, pointer):
    data = new_dict_without_key(full_data, property)

    expected_error = {
        "id": "CM_MISSING_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Missing property",
        "detail": "The property at the specified location is required, but was not present in the request.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={**nhsd_apim_auth_headers, **headers},
        json=data,
    )

    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")


@pytest.mark.prodtest
@pytest.mark.parametrize(
    "property, pointer",
    _missing_properties
)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_property_missing_prod_with_correlation_id(nhsd_apim_proxy_url, nhsd_apim_auth_headers, property, pointer):
    data = new_dict_without_key(full_data, property)

    expected_error = {
        "id": "CM_MISSING_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Missing property",
        "detail": "The property at the specified location is required, but was not present in the request.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **nhsd_apim_auth_headers,
            **headers,
            "X-Correlation-Id": x_correlation_id_value
        },
        json=data,
    )

    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")
    assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value


"""
Null data 400 test
"""

_null_properties = [
    ("data", "/data"),
    ("attributes", "/data/attributes"),
    ("recipient", "/data/attributes/messages/0/recipient"),
]


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    _null_properties
)
def test_data_null_sandbox(nhsd_apim_proxy_url, property, pointer):
    data = new_dict_with_null_key(full_data, property)
    expected_error = {
        "id": "CM_NULL_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Property cannot be null",
        "detail": "The property at the specified location is required, but a null value was passed in the request.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers=headers,
        json=data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    _null_properties
)
def test_data_null_sandbox_with_correlation_id(nhsd_apim_proxy_url, property, pointer):
    data = new_dict_with_null_key(full_data, property)
    expected_error = {
        "id": "CM_NULL_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Property cannot be null",
        "detail": "The property at the specified location is required, but a null value was passed in the request.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": x_correlation_id_value
        },
        json=data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")
    assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value


@pytest.mark.prodtest
@pytest.mark.parametrize(
    "property, pointer",
    _null_properties
)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_data_null_prod(nhsd_apim_proxy_url, nhsd_apim_auth_headers, property, pointer):
    data = new_dict_with_null_key(full_data, property)
    expected_error = {
        "id": "CM_NULL_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Property cannot be null",
        "detail": "The property at the specified location is required, but a null value was passed in the request.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={**nhsd_apim_auth_headers, **headers},
        json=data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")


@pytest.mark.prodtest
@pytest.mark.parametrize(
    "property, pointer",
    _null_properties
)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_data_null_prod_with_correlation_id(nhsd_apim_proxy_url, nhsd_apim_auth_headers, property, pointer):
    data = new_dict_with_null_key(full_data, property)
    expected_error = {
        "id": "CM_NULL_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Property cannot be null",
        "detail": "The property at the specified location is required, but a null value was passed in the request.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **nhsd_apim_auth_headers,
            **headers,
            "X-Correlation-Id": x_correlation_id_value
        },
        json=data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")
    assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value


"""
Invalid data 400 test
"""

_invalid_properties = [
    ("type", "/data/type"),
    ("routingPlanId", "/data/attributes/routingPlanId"),
    ("messageBatchReference", "/data/attributes/messageBatchReference"),
    ("messages", "/data/attributes/messages"),
    ("messageReference", "/data/attributes/messages/0/messageReference"),
    ("recipient", "/data/attributes/messages/0/recipient"),
    ("nhsNumber", "/data/attributes/messages/0/recipient/nhsNumber"),
    ("dateOfBirth", "/data/attributes/messages/0/recipient/dateOfBirth"),
    ("personalisation", "/data/attributes/messages/0/personalisation"),
]


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    _invalid_properties
)
def test_data_invalid_sandbox(nhsd_apim_proxy_url, property, pointer):
    data = new_dict_with_new_value(full_data, property, "invalid string")
    expected_error = {
        "id": "CM_INVALID_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Invalid value",
        "detail": "The property at the specified location does not allow this value.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers=headers,
        json=data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    _invalid_properties
)
def test_data_invalid_sandbox_with_correlation_id(nhsd_apim_proxy_url, property, pointer):
    data = new_dict_with_new_value(full_data, property, "invalid string")
    expected_error = {
        "id": "CM_INVALID_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Invalid value",
        "detail": "The property at the specified location does not allow this value.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": x_correlation_id_value
        },
        json=data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")
    assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value


@pytest.mark.prodtest
@pytest.mark.parametrize(
    "property, pointer",
    _invalid_properties
)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_data_invalid_prod(nhsd_apim_proxy_url, nhsd_apim_auth_headers, property, pointer):
    data = new_dict_with_new_value(full_data, property, "invalid string")
    expected_error = {
        "id": "CM_INVALID_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Invalid value",
        "detail": "The property at the specified location does not allow this value.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={**nhsd_apim_auth_headers, **headers},
        json=data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")


@pytest.mark.prodtest
@pytest.mark.parametrize(
    "property, pointer",
    _invalid_properties
)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_data_invalid_prod_with_correlation_id(nhsd_apim_proxy_url, nhsd_apim_auth_headers, property, pointer):
    data = new_dict_with_new_value(full_data, property, "invalid string")
    expected_error = {
        "id": "CM_INVALID_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Invalid value",
        "detail": "The property at the specified location does not allow this value.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **nhsd_apim_auth_headers,
            **headers,
            "X-Correlation-Id": x_correlation_id_value
        },
        json=data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")
    assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value


"""
Duplicate data 400 test
"""

_duplicate_properties = [
    ("messageReference", "/data/attributes/messages/1/messageReference"),
]


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    _duplicate_properties
)
def test_data_duplicate_sandbox(nhsd_apim_proxy_url, property, pointer):
    data = full_data
    # Add a duplicate message to the payload to trigger the duplicate error
    data["data"]["attributes"]["messages"].append(
        {
          "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
          "recipient": {
            "nhsNumber": "1234567890",
            "dateOfBirth": "1982-03-17"
          },
          "personalisation": {}
        }
    )
    expected_error = {
        "id": "CM_DUPLICATE_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Duplicate value",
        "detail": "The property at the specified location is a duplicate, duplicated values are not allowed.",
        "source": {
            "pointer": pointer
        }
    }
    # Post the same message a 2nd time to trigger the duplicate error
    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers=headers,
        json=full_data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    _duplicate_properties
)
def test_data_duplicate_sandbox_with_correlation_id(nhsd_apim_proxy_url, property, pointer):
    data = full_data
    # Add a duplicate message to the payload to trigger the duplicate error
    data["data"]["attributes"]["messages"].append(
        {
          "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
          "recipient": {
            "nhsNumber": "1234567890",
            "dateOfBirth": "1982-03-17"
          },
          "personalisation": {}
        }
    )
    expected_error = {
        "id": "CM_DUPLICATE_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Duplicate value",
        "detail": "The property at the specified location is a duplicate, duplicated values are not allowed.",
        "source": {
            "pointer": pointer
        }
    }
    # Post the same message a 2nd time to trigger the duplicate error
    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": x_correlation_id_value
        },
        json=full_data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")
    assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value


@pytest.mark.prodtest
@pytest.mark.parametrize(
    "property, pointer",
    _duplicate_properties
)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_data_duplicate_prod(nhsd_apim_proxy_url, nhsd_apim_auth_headers, property, pointer):
    data = full_data
    # Add a duplicate message to the payload to trigger the duplicate error
    data["data"]["attributes"]["messages"].append(
        {
          "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
          "recipient": {
            "nhsNumber": "1234567890",
            "dateOfBirth": "1982-03-17"
          },
          "personalisation": {}
        }
    )
    expected_error = {
        "id": "CM_DUPLICATE_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Duplicate value",
        "detail": "The property at the specified location is a duplicate, duplicated values are not allowed.",
        "source": {
            "pointer": pointer
        }
    }
    # Post the same message a 2nd time to trigger the duplicate error
    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={**nhsd_apim_auth_headers, **headers},
        json=full_data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")


@pytest.mark.prodtest
@pytest.mark.parametrize(
    "property, pointer",
    _duplicate_properties
)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_data_duplicate_prod_with_correlation_id(nhsd_apim_proxy_url, nhsd_apim_auth_headers, property, pointer):
    data = full_data
    # Add a duplicate message to the payload to trigger the duplicate error
    data["data"]["attributes"]["messages"].append(
        {
          "messageReference": "703b8008-545d-4a04-bb90-1f2946ce1575",
          "recipient": {
            "nhsNumber": "1234567890",
            "dateOfBirth": "1982-03-17"
          },
          "personalisation": {}
        }
    )
    expected_error = {
        "id": "CM_DUPLICATE_VALUE",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Duplicate value",
        "detail": "The property at the specified location is a duplicate, duplicated values are not allowed.",
        "source": {
            "pointer": pointer
        }
    }
    # Post the same message a 2nd time to trigger the duplicate error
    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **nhsd_apim_auth_headers,
            **headers,
            "X-Correlation-Id": x_correlation_id_value
        },
        json=full_data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")
    assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value


"""
Too few items 400 test
"""

_too_few_properties = [
    ("messages", "/data/attributes/messages"),
]


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    _too_few_properties
)
def test_data_too_few_items_sandbox(nhsd_apim_proxy_url, property, pointer):
    data = new_dict_with_new_value(full_data, property, [])
    expected_error = {
        "id": "CM_TOO_FEW_ITEMS",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Too few items",
        "detail": "The property at the specified location contains too few items.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers=headers,
        json=data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")


@pytest.mark.sandboxtest
@pytest.mark.parametrize(
    "property, pointer",
    _too_few_properties
)
def test_data_too_few_items_sandbox_with_correlation_id(nhsd_apim_proxy_url, property, pointer):
    data = new_dict_with_new_value(full_data, property, [])
    expected_error = {
        "id": "CM_TOO_FEW_ITEMS",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Too few items",
        "detail": "The property at the specified location contains too few items.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **headers,
            "X-Correlation-Id": x_correlation_id_value
        },
        json=data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")
    assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value


@pytest.mark.prodtest
@pytest.mark.parametrize(
    "property, pointer",
    _too_few_properties
)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_data_too_few_items_prod(nhsd_apim_proxy_url, nhsd_apim_auth_headers, property, pointer):
    data = new_dict_with_new_value(full_data, property, [])
    expected_error = {
        "id": "CM_TOO_FEW_ITEMS",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Too few items",
        "detail": "The property at the specified location contains too few items.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={**nhsd_apim_auth_headers, **headers},
        json=data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")


@pytest.mark.prodtest
@pytest.mark.parametrize(
    "property, pointer",
    _too_few_properties
)
@pytest.mark.nhsd_apim_authorization({"access": "application", "level": "level3"})
def test_data_too_few_items_prod_with_correlation_id(nhsd_apim_proxy_url, nhsd_apim_auth_headers, property, pointer):
    data = new_dict_with_new_value(full_data, property, [])
    expected_error = {
        "id": "CM_TOO_FEW_ITEMS",
        "links": {
            "about": "https://digital.nhs.uk/developer/api-catalogue/communications-manager"
        },
        "status": "400",
        "title": "Too few items",
        "detail": "The property at the specified location contains too few items.",
        "source": {
            "pointer": pointer
        }
    }

    resp = requests.post(
        f"{nhsd_apim_proxy_url}/v1/message-batches",
        headers={
            **nhsd_apim_auth_headers,
            **headers,
            "X-Correlation-Id": x_correlation_id_value
        },
        json=data,
    )
    assert resp.status_code == 400
    assert expected_error in resp.json().get("errors")
    assert resp.headers.get("X-Correlation-Id") == x_correlation_id_value


def new_dict_without_key(input_dict, key):
    if isinstance(input_dict, dict):
        return {k: new_dict_without_key(v, key) for k, v in input_dict.items() if k != key}
    elif isinstance(input_dict, list):
        return [new_dict_without_key(element, key) for element in input_dict]
    else:
        return input_dict


def new_dict_with_null_key(input_dict, key):
    if isinstance(input_dict, dict):
        return {k: new_dict_with_null_key(v, key) if k != key else None for k, v in input_dict.items()}
    elif isinstance(input_dict, list):
        return [new_dict_with_null_key(element, key) for element in input_dict]
    else:
        return input_dict


def new_dict_with_new_value(input_dict, key, new_value):
    if isinstance(input_dict, dict):
        return {
            k: new_dict_with_new_value(v, key, new_value) if k != key
            else new_value for k, v in input_dict.items()
        }
    elif isinstance(input_dict, list):
        return [new_dict_with_new_value(element, key, new_value) for element in input_dict]
    else:
        return input_dict
