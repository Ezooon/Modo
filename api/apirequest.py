from kivy.network.urlrequest import UrlRequest
from kivymd.app import MDApp
import json

HOST = 'http://127.0.0.1:8000/'


def add_url_params(params):
    string = '?'
    for parm in params:
        string += parm + '=' + str(params[parm]) + '&'
    return string[:-1]


def api_request(url, on_success, params={}, on_failure=print, method='GET', body=None, headers=None, on_finish=None):
    params = add_url_params({'format': 'json', **params})
    login = MDApp.get_running_app().user_api_token
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

    UrlRequest(HOST + "api/" + url + params, on_success, on_failure=on_failure, method=method, req_body=body,
               req_headers=headers, debug=True, on_error=on_failure, on_finish=on_finish)

