from rest_framework.test import APIClient


def test_general(url, request, method):
    client = APIClient()
    if method == 'post':
        response = client.post(url, request, format='json')
    elif method == 'get':
        response = client.get(url, request, format='json')
    else:
        response = client.put(url, request, format='json')
    return response.status_code, response
