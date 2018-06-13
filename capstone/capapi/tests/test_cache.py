import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize("view_name, cache_if_logged_out, cache_if_logged_in, get_kwargs", [
    # docs pages are cached for both logged in and logged out
    ("home",                True,   True,  {}),

    # pages with csrf tokens are not cached for logged out or logged in
    ("login",               False,  False,  {}),
    ("register",            False,  False,  {}),

    # login-only pages are cached only for logged out (where they redirect)
    ("user-details",        True,   False, {}),

    # api views are cached for both logged in and logged out
    ("casemetadata-list",   True,   True,   {}),
    ("casemetadata-list",   True,   True,   {"HTTP_ACCEPT": "text/html"}),

    # api views that depend on the user account are cached only for logged out
    ("casemetadata-list",   True,   False,  {"data": {"full_case": "true"}}),
])
@pytest.mark.parametrize("client_fixture_name", ["client", "auth_client"])
def test_cache_headers(case, request, settings,
                       client_fixture_name,
                       view_name, cache_if_logged_out, cache_if_logged_in, get_kwargs):

    # set up variables
    settings.SET_CACHE_CONTROL_HEADER = True
    url = reverse(view_name)
    client = request.getfuncargvalue(client_fixture_name)
    cache_expected = cache_if_logged_in if client._credentials else cache_if_logged_out

    # see if response is cached
    response = client.get(url, **get_kwargs)
    cache_header = response['cache-control'] if response.has_header('cache-control') else ''
    cache_actual = 's-maxage=%d' % settings.CACHE_CONTROL_DEFAULT_MAX_AGE in cache_header

    assert cache_actual == cache_expected, "Checking %s with %s, expected %scached but found %scached." % (
        url,
        client_fixture_name,
        "" if cache_expected else "not ",
        "" if cache_actual else "not ",
    )