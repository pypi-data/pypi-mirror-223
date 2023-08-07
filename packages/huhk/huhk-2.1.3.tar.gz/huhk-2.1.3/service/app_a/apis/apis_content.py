import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/adv/")
def content_adv_(advId=None, headers=None, **kwargs):
    """
    点位内容-通过id删除点位内容-Y
    up_time=1675674580

    params: advId :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : integer : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "DELETE"
    _url = "/content/adv/{advId}"
    _url = get_url(_url, locals())

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "advId": advId,
    }

    _params = {
        "advId": advId,
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


