import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/radarpoints/userPoints/exchangeInfo/pageList")
def radarpoints_userpoints_exchangeinfo_pagelist(userId=None, orderEndTime=None, consigneeName=None, current=None, goodsOrderId=None, orderStartTime=None, mobile=None, size=None, headers=None, **kwargs):
    """
    用户中心-兑换明细 - 分页查询
    up_time=1676903335

    params: size :  : 每页大小
    params: current :  : 当前页
    params: userId :  : 用户ID
    params: consigneeName :  : 收货人姓名
    params: goodsOrderId :  : 商品订单
    params: mobile :  : 收货人电话
    params: orderStartTime :  : 下单开始时间
    params: orderEndTime :  : 下单结束时间
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              records : array : 
              size : number : 每页大小
              current : number : 当前页
              total : number : 总页数
    """
    _method = "GET"
    _url = "/radarpoints/userPoints/exchangeInfo/pageList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "size": size,  # 每页大小
        "current": current,  # 当前页
        "userId": userId,  # 用户ID
        "consigneeName": consigneeName,  # 收货人姓名
        "goodsOrderId": goodsOrderId,  # 商品订单
        "mobile": mobile,  # 收货人电话
        "orderStartTime": orderStartTime,  # 下单开始时间
        "orderEndTime": orderEndTime,  # 下单结束时间
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


