import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/common/common/getChannel")
def common_common_getchannel( headers=None, **kwargs):
    """
    文章-获取发布渠道-Y
    up_time=1675323365

    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : array : 
              channelId : number : 渠道主键
              channelName : string : 渠道名称
              status : integer : 状态码1：可用0：不可用
              createBy : number : 
              createTime : string : 
              updateBy : number : 
              updateTime : string : 
    """
    _method = "GET"
    _url = "/common/common/getChannel"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


