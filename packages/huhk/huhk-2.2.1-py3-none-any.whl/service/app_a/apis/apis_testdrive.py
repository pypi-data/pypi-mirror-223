import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/testDrive/subscribe")
def testdrive_subscribe(appointmentTime=None, customerName=None, modelId=None, shopId=None, channel=None, leadSanSourceCode=None, leadSourceCode=None, shopName=None, model=None, activityCode=None, phoneNumber=None, headers=None, **kwargs):
    """
    预约试驾
    up_time=1689560965

    params: model : text : 试驾车型名称
    params: shopName : text : 门店名称
    params: customerName : text : 客户姓名、昵称
    params: phoneNumber : text : 预留手机号
    params: channel : text : 1:移动应用 2:小程序 3:官方网站
    params: modelId : text : 预约车型id
    params: shopId : text : 预约门店id
    params: appointmentTime : text : 预约时间
    params: activityCode : string : 活动代码
    params: leadSourceCode : string : 线索来源小类
    params: leadSanSourceCode : string : 线索来源三级小类
    params: headers : 请求头
    ====================返回======================
    params: code : string : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/testDrive/subscribe"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "model": model,  # 试驾车型名称
        "shopName": shopName,  # 门店名称
        "customerName": customerName,  # 客户姓名、昵称
        "phoneNumber": phoneNumber,  # 预留手机号
        "channel": channel,  # 1:移动应用 2:小程序 3:官方网站
        "modelId": modelId,  # 预约车型id
        "shopId": shopId,  # 预约门店id
        "appointmentTime": appointmentTime,  # 预约时间
        "activityCode": activityCode,  # 活动代码
        "leadSourceCode": leadSourceCode,  # 线索来源小类
        "leadSanSourceCode": leadSanSourceCode,  # 线索来源三级小类
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


