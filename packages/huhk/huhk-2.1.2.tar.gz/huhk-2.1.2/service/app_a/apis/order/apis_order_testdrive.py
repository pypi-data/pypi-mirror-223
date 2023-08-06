import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/order/testDrive/exportList")
def order_testdrive_exportlist(id=None, shopName=None, createTime=None, createByName=None, channel=None, startTime=None, endTime=None, phoneNumber=None, headers=None, **kwargs):
    """
    导出试驾表单-Y
    up_time=1675417182

    params: phoneNumber :  : 手机号
    params: createByName :  : 
    params: id :  : 主键
    params: channel :  : 渠道(1:移动应用 2:小程序 3:官方网站)
    params: startTime :  : 
    params: endTime :  : 
    params: shopName :  : 门店名称
    params: createTime :  : 创建时间
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/order/testDrive/exportList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "phoneNumber": phoneNumber,  # 手机号
        "createByName": createByName,
        "id": id,  # 主键
        "channel": channel,  # 渠道(1:移动应用 2:小程序 3:官方网站)
        "startTime": startTime,
        "endTime": endTime,
        "shopName": shopName,  # 门店名称
        "createTime": createTime,  # 创建时间
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/testDrive/userList")
def order_testdrive_userlist(current=None, createBy=None, size=None, modelId=None, headers=None, **kwargs):
    """
    用户中心-预约信息
    up_time=1675417772

    params: current :  : 当前页数
    params: size :  : 每页数据数
    params: createBy :  : 
    params: modelId :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              records : array : 
              total : string : 
              size : string : 
              current : string : 
    """
    _method = "GET"
    _url = "/order/testDrive/userList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,  # 当前页数
        "size": size,  # 每页数据数
        "createBy": createBy,
        "modelId": modelId,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


