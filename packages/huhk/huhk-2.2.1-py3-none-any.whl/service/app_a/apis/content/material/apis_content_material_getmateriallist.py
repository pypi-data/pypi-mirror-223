import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/material/getMaterialList_1659319316474")
def content_material_getmateriallist_1659319316474(current=None, groupId=None, size=None, headers=None, **kwargs):
    """
    素材-根据素材组获取素材列表_copy
    up_time=1675755133

    params: groupId :  : 分组主键
    params: size :  : 每页数据数
    params: current :  : 当前页
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              records : array : 
              total : number : 
              size : number : 
              current : number : 
              orders : array : 
              optimizeCountSql : boolean : 
              searchCount : boolean : 
              countId : null : 
              maxLimit : null : 
              pages : number : 
    """
    _method = "GET"
    _url = "/content/material/getMaterialList_1659319316474"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "groupId": groupId,  # 分组主键
        "size": size,  # 每页数据数
        "current": current,  # 当前页
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


