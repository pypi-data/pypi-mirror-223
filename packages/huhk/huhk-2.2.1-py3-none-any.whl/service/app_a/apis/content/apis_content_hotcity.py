import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/hotcity/list")
def content_hotcity_list( headers=None, **kwargs):
    """
    热门城市-Y
    up_time=1675390336

    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : array : 
              id : number : ID主键
              name : string : 城市名称
              areaId : number : 城市代码
    """
    _method = "GET"
    _url = "/content/hotcity/list"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


