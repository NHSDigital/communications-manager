import requests
import pytest
from lib import Assertions, Generators
from lib.constants.user_details_paths import USER_DETAILS_ENDPOINT, ODS_CODE_PARAM_NAME, PAGE_PARAM_NAME, \
    VALID_ODS_CODES

INVALID_PAGE_NUMBERS = [2, 3, 4, 5, 6]
CORRELATION_IDS = [None, "228aac39-542d-4803-b28e-5de9e100b9f8"]


@pytest.mark.sandboxtest
@pytest.mark.parametrize("ods_code", VALID_ODS_CODES)
@pytest.mark.parametrize("page", INVALID_PAGE_NUMBERS)
@pytest.mark.parametrize("correlation_id", CORRELATION_IDS)
def test_404_page_not_found(nhsd_apim_proxy_url, ods_code, page, correlation_id):

    resp = requests.get(f"{nhsd_apim_proxy_url}{USER_DETAILS_ENDPOINT}", headers={
        "X-Correlation-Id": correlation_id,
        "Accept": "application/vnd.api+json"
    }, params={
        ODS_CODE_PARAM_NAME: ods_code,
        PAGE_PARAM_NAME: page
    })

    Assertions.assert_error_with_optional_correlation_id(
        resp,
        404,
        Generators.generate_not_found_error(),
        correlation_id
        )