from django.test import Client


def test_general(url, request, method):
    c = Client()
    if method == 'post':
        response = c.post(url, request)
    elif method == 'get':
        response = c.get(url, request)
    else:
        response = c.put(url, request)
    return response.status_code, response
