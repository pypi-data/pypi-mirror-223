import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/order/freeOrder/downLoad")
def order_freeorder_download(provinceName=None, freeOrderId=None, provinceId=None, regisTimeBegin=None, avatarUrl=None, createTime=None, nickName=None, modelId=None, userPolicyCode=None, channel=None, privacyPolicyCode=None, mobile=None, cityName=None, channelName=None, regisTimeEnd=None, cityId=None, userName=None, headers=None, **kwargs):
    """
    导出0元订购预定信息表-Y
    up_time=1675318920

    params: freeOrderId : integer : 订单号
    params: modelId : string : 车型编码
    params: userName : string : 用户姓名
    params: mobile : string : 用户号码
    params: provinceId : string : 省编码
    params: provinceName : string : 省
    params: cityId : string : 市编码
    params: cityName : string : 市
    params: channel : string : 渠道 0 官网 1 app
    params: channelName : string : 
    params: createTime : string : 订单创建时间
    params: regisTimeBegin : string : 开始时间
    params: regisTimeEnd : string : 结束时间
    params: nickName : string : 昵称
    params: avatarUrl : string : 头像
    params: userPolicyCode : string : 用户协议版本号
    params: privacyPolicyCode : string : 隐私协议版本号
    params: headers : 请求头
    ====================返回======================
    """
    _method = "POST"
    _url = "/order/freeOrder/downLoad"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "freeOrderId": freeOrderId,  # 订单号
        "modelId": modelId,  # 车型编码
        "userName": userName,  # 用户姓名
        "mobile": mobile,  # 用户号码
        "provinceId": provinceId,  # 省编码
        "provinceName": provinceName,  # 省
        "cityId": cityId,  # 市编码
        "cityName": cityName,  # 市
        "channel": channel,  # 渠道 0 官网 1 app
        "channelName": channelName,
        "createTime": createTime,  # 订单创建时间
        "regisTimeBegin": regisTimeBegin,  # 开始时间
        "regisTimeEnd": regisTimeEnd,  # 结束时间
        "nickName": nickName,  # 昵称
        "avatarUrl": avatarUrl,  # 头像
        "userPolicyCode": userPolicyCode,  # 用户协议版本号
        "privacyPolicyCode": privacyPolicyCode,  # 隐私协议版本号
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


