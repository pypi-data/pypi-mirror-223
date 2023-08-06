import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/common/user/getUserVestList")
def common_user_getuservestlist( headers=None, **kwargs):
    """
    获取管理后台用户的小号（马甲）-Y
    up_time=1675649144

    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : array : 
              id : string : 用户Id
              name : string : 用户昵称
    """
    _method = "GET"
    _url = "/common/user/getUserVestList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


