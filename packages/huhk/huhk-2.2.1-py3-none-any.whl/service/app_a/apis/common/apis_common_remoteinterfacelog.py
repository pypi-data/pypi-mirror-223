import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/common/remoteinterfacelog/getLogPage")
def common_remoteinterfacelog_getlogpage(current=None, mobile=None, startTime=None, endTime=None, interfaceType=None, userName=None, size=None, headers=None, **kwargs):
    """
    查询三方日志接口-Y
    up_time=1675324564

    params: interfaceType :  : 日志类型（1.支付日志  2.退款日志  3.换电日志）
    params: startTime :  : 开始时间
    params: endTime :  : 结束时间
    params: userName :  : 用户昵称
    params: mobile :  : 手机号
    params: size :  : 每页条数
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
              countId : number : 
              maxLimit : number : 
              pages : number : 
    """
    _method = "GET"
    _url = "/common/remoteinterfacelog/getLogPage"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "interfaceType": interfaceType,  # 日志类型（1.支付日志  2.退款日志  3.换电日志）
        "startTime": startTime,  # 开始时间
        "endTime": endTime,  # 结束时间
        "userName": userName,  # 用户昵称
        "mobile": mobile,  # 手机号
        "size": size,  # 每页条数
        "current": current,  # 当前页
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


