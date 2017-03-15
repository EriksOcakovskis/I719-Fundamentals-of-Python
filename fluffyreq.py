import requests
import json


def post_json_to_server(url, data):
    response = -1
    try:
        data_json = json.dumps(data)
        print(data_json)
        s = requests.Session()
        req = requests.Request('POST', url, data=data_json)
        prepped = req.prepare()
        prepped.headers['Content-Type'] = 'application/json'
        response = s.send(prepped).status_code
    except Exception as e:
        raise e
    finally:
        return response


def get_host_ip(inp_ip):
    try:
        r = requests.get(inp_ip)
        resp = r.status_code
        ip = r.text
        return ({'ip': ip, 'status code': resp})
    except Exception as e:
        raise e
