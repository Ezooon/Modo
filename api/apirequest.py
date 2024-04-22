from kivy.network.urlrequest import UrlRequest
import json

login = ''
HOST = 'http://127.0.0.1:8000/api/'


def add_url_params(params):
    string = '?'
    for parm in params:
        string += parm + '=' + str(params[parm]) + '&'
    return string[:-1]


def api_request(url, on_success, params=dict(), on_failure=print, method='GET', body=None, headers=None):
    params = add_url_params({'format': 'json', **params})
    if login:
        heads = headers or {}
        headers = {'Authorization': 'Token '+login, **heads}

    if body:
        body = json.dumps(body, indent=4)
        heads = headers or {}
        headers = {**heads,
                   'Content-Type': 'Application/json',
                   'Content-length': len(body)
                   }
    UrlRequest(HOST + url + params, on_success, on_failure=on_failure, method=method, req_body=body,
               req_headers=headers, debug=True)
