import requests


def api_list(endpoint, _check_object=True):
    resp = requests.get(endpoint)
    if _check_object:
        return has_response_object(resp)
    else:
        return has_response(resp)


def api_view(endpoint, uuid, _check_object=True):
    resp = requests.get(f'{endpoint}/{uuid}')
    if _check_object:
        return has_response_object(resp)
    else:
        return has_response(resp)


def api_create(endpoint, data, _check_object=True):
    resp = requests.post(f'{endpoint}', json=data,
                                            headers={'Content-type': 'application/json', 'Accept': 'application/json'})
    if _check_object:
        return has_response_object(resp)
    else:
        return has_response(resp)


def api_update(endpoint, uuid, data, _check_object=True):
    resp = requests.post(f'{endpoint}/{uuid}', json=data,
                                            headers={'Content-type': 'application/json', 'Accept': 'application/json'})
    if _check_object:
        return has_response_object(resp)
    else:
        return has_response(resp)


def api_delete(endpoint, uuid, _check_object=True):
    resp = requests.delete(f'{endpoint}/{uuid}')
    if _check_object:
        return has_response_object(resp)
    else:
        return has_response(resp)
    

def has_response(resp):
    res = resp.json()
    assert resp.status_code == 200
    assert 'status' in res
    assert 'count' in res
    assert 'data' in res
    return res


def has_response_object(resp):
    res = resp.json()
    assert resp.status_code == 200
    assert 'status' in res
    assert 'count' in res
    assert 'data' in res
    if res['count'] == 1:
        assert 'id' in res['data']
        assert 'uuid' in res['data']
    elif res['count'] > 1:
        assert 'id' in res['data'][0]
        assert 'uuid' in res['data'][0]
    return res
