import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/common/clue/getClueUserPage")
def common_clue_getclueuserpage(current=None, userId=None, size=None, headers=None, **kwargs):
    """
    用户列表-详情-查询线索-Y
    up_time=1675318572

    params: current :  : 页码
    params: size :  : 每页大小
    params: userId :  : 用户ID
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
              countId : string : 
              maxLimit : number : 
              pages : number : 
              field_66 : string : 
    """
    _method = "GET"
    _url = "/common/clue/getClueUserPage"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,  # 页码
        "size": size,  # 每页大小
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


