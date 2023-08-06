import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/admin/spa/getAppId")
def admin_spa_getappid( headers=None, **kwargs):
    """
    获取guc appId
    up_time=1675133803

    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功
    params: msg : string : 描述
    params: data : object : 返回
              appId : string : appid
    """
    _method = "GET"
    _url = "/admin/spa/getAppId"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


