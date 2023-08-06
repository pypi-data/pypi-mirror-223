import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/admin/guc/gucLogout")
def admin_guc_guclogout( headers=None, **kwargs):
    """
    guc登出
    up_time=1675133803

    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功
    params: msg : string : 描述
    params: data : object : 返回
              result : boolean : true成功
    """
    _method = "POST"
    _url = "/admin/guc/gucLogout"

    _headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/admin/guc/gucLogin")
def admin_guc_guclogin( headers=None, **kwargs):
    """
    guc登录回调
    up_time=1675133803

    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功
    params: msg : string : 描述
    params: data : object : 返回
              result : boolean : true成功
    """
    _method = "POST"
    _url = "/admin/guc/gucLogin"

    _headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


