import pytest
import os
from .authentication import AuthenticationCache
from .app_keys import ensure_api_product_in_application, ensure_api_product_not_in_application
from .rate_limiting import RateLimiting
from lib.constants.constants import INT_URL, PROD_URL


@pytest.fixture(scope='session')
def proxy_name():
    try:
        return os.environ['API_PROXY']
    except KeyError:
        # fall back to PROXY_NAME
        return os.environ['PROXY_NAME']


# for now this is the same as PROXY_NAME
# this is here to illustrate how these can be decoupled
@pytest.fixture(scope='session')
def api_product_name():
    try:
        return os.environ['API_PROXY']
    except KeyError:
        # fall back to PROXY_NAME
        return os.environ['PROXY_NAME']


# define one of these for each key we have set up and intend to use
@pytest.fixture(scope='session')
def api_product_in_comms_manager_local(developer_app_keys_api, api_product_name):
    if api_product_name.startswith('communications-manager-pr-'):
        yield ensure_api_product_in_application(
                developer_app_keys_api,
                'phillip.skinner2@nhs.net',
                'Comms-manager-local',
                os.environ['NON_PROD_API_KEY'],
                api_product_name)
        ensure_api_product_not_in_application(
                developer_app_keys_api,
                'phillip.skinner2@nhs.net',
                'Comms-manager-local',
                os.environ['NON_PROD_API_KEY'],
                api_product_name)
    else:
        yield None


@pytest.fixture(scope='session')
def api_product_in_nhs_notify_test_client_1(developer_app_keys_api, api_product_name):
    if api_product_name.startswith('communications-manager-pr-'):
        yield ensure_api_product_in_application(
                developer_app_keys_api,
                'ian.hodges1@nhs.net',
                'NHS Notify Test Client 1',
                os.environ['NON_PROD_API_KEY_TEST_1'],
                api_product_name)
        ensure_api_product_not_in_application(
                developer_app_keys_api,
                'ian.hodges1@nhs.net',
                'NHS Notify Test Client 1',
                os.environ['NON_PROD_API_KEY_TEST_1'],
                api_product_name)
    else:
        yield None


# By setting the scope to session on the cache but leaving session scope OFF
# the fixtures for each bearer token, we ensure the cache is checked and has a
# chance to refresh before any test which might depend on a bearer token
@pytest.fixture(scope='session')
def authentication_cache():
    return AuthenticationCache()


@pytest.fixture
def bearer_token_internal_dev(authentication_cache, api_product_in_comms_manager_local, nhsd_apim_proxy_url):
    return authentication_cache.generate_authentication('internal-dev', nhsd_apim_proxy_url)


@pytest.fixture
def bearer_token_internal_dev_test_1(authentication_cache,
                                     api_product_in_nhs_notify_test_client_1,
                                     nhsd_apim_proxy_url):
    return authentication_cache.generate_authentication('internal-dev-test-1', nhsd_apim_proxy_url)


@pytest.fixture
def bearer_token_int(authentication_cache):
    return authentication_cache.generate_authentication('int', INT_URL)


@pytest.fixture
def bearer_token_prod(authentication_cache):
    return authentication_cache.generate_authentication('prod', PROD_URL)


@pytest.fixture(scope='session')
def rate_limiting(products_api, api_product_name, developer_apps_api):
    rate_limiting = RateLimiting(products_api, developer_apps_api, api_product_name, 5)
    yield rate_limiting
    rate_limiting.set_default_rate_limit()
