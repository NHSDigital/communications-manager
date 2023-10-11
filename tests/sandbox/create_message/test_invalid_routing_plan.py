import requests
import pytest
import uuid
from lib import Assertions, Generators


CORRELATION_IDS = [None, "228aac39-542d-4803-b28e-5de9e100b9f8"]
DUPLICATE_ROUTING_PLAN_TEMPLATE_ID = "a3a4e55d-7a21-45a6-9286-8eb595c872a8"


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_500_routing_plan_with_duplicate_templates(nhsd_apim_proxy_url, correlation_id):
    """
    .. include:: ../../partials/invalid_routing_plans/test_500_duplicate_routing_plan.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/messages", headers={
        "X-Correlation-Id": correlation_id
    }, json={
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": DUPLICATE_ROUTING_PLAN_TEMPLATE_ID,
                "messageReference": str(uuid.uuid1()),
                "recipient": {
                    "nhsNumber": "9990548609",
                    "dateOfBirth": "1982-03-17"
                },
                "personalisation": {}
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        500,
        Generators.generate_duplicate_routing_plan_template_error([
            {
                "name": "EMAIL_TEMPLATE",
                "type": "EMAIL"
            },
            {
                "name": "SMS_TEMPLATE",
                "type": "SMS"
            },
            {
                "name": "LETTER_TEMPLATE",
                "type": "LETTER"
            },
            {
                "name": "LETTER_PDF_TEMPLATE",
                "type": "LETTER_PDF"
            },
            {
                "name": "NHSAPP_TEMPLATE",
                "type": "NHSAPP"
            }
        ]),
        correlation_id
    )


@pytest.mark.sandboxtest
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
@pytest.mark.parametrize("routing_plan_id", [
    "c8857ccf-06ec-483f-9b3a-7fc732d9ad48",
    "aeb16ab8-cb9c-4d23-92e9-87c78119175c"
])
def test_500_routing_plan_with_missing_template(nhsd_apim_proxy_url, correlation_id, routing_plan_id):
    """
    .. include:: ../../partials/invalid_routing_plans/test_500_missing_routing_plan.rst
    """
    resp = requests.post(f"{nhsd_apim_proxy_url}/v1/messages", headers={
        "X-Correlation-Id": correlation_id
    }, json={
        "data": {
            "type": "Message",
            "attributes": {
                "routingPlanId": routing_plan_id,
                "messageReference": str(uuid.uuid1()),
                "recipient": {
                    "nhsNumber": "9990548609",
                    "dateOfBirth": "1982-03-17"
                },
                "personalisation": {}
            }
        }
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        500,
        Generators.generate_missing_routing_plan_template_error(),
        correlation_id
    )