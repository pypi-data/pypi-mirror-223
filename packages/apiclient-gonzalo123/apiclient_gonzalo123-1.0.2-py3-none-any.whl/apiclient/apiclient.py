import requests


class ApiClientException(Exception):
    pass


class ApiClientAuthException(Exception):
    pass


class ApiClient:
    def __init__(self, token, base):
        self.token = token
        self.base = base

    @staticmethod
    def _zip(columns, rows):
        return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def _get_headers(token):
        return {
            'token': token,
            'x-client': 'apiclient',
            'Content-Type': 'application/json'
        }

    def _get_url(self, uri):
        return f'{self.base}{uri}'

    def _process_response(self, response):
        if response.ok:
            data = response.json()
            if response.headers['x-recordset'] == 'compact':
                return self._zip(*data)
            else:
                return data
        elif response.status_code == 401:
            raise ApiClientAuthException('not valid token')
        else:
            raise ApiClientException(response.json())

    def get(self, uri, params):
        return self._process_response(requests.get(
            url=self._get_url(uri),
            params=params,
            headers=self._get_headers(self.token)))

    def post(self, uri, params=None, body=None):
        return self._process_response(requests.post(
            url=self._get_url(uri),
            params=params,
            json=body,
            headers=self._get_headers(self.token)))
