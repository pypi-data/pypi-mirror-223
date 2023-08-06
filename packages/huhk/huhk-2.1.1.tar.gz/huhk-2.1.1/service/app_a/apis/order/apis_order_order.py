import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/order/order/orderDetail")
def order_order_orderdetail(userId=None, orderStatus=None, total=None, pageSize=None, pageNum=None, orderId=None, headers=None, **kwargs):
    """
    订单详情
    up_time=1675133817

    params: orderId :  : 订单主单Id
    params: userId :  : 用户ID
    params: orderStatus : string : 订单状态
    params: pageSize : number : 每页大小
    params: pageNum : number : 当前页
    params: total : number : 总数
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              orderId : string : 订单主单ID
              orderStatus : string : 
              orderStatusName : string : 
              createTime : string : 
              userName : string : 下单人名称
              mobile : string : 
              prePrice : string : 定金
              totalPrice : string : 总价
              model : object : 
              battery : object : 
              modelPic : object : 
              shopVo : object : 
              itemList : array : 
              areaName : string : 上牌城市
              price : number : 
              pageNum : number : 
              total : number : 
    """
    _method = "GET"
    _url = "/order/order/orderDetail{orderId}{userId}"

    _headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    _headers.update({"headers": headers})

    _data = {
        "orderId": orderId,  # 订单主单ID
        "orderStatus": orderStatus,  # 订单状态
        "pageSize": pageSize,  # 每页大小
        "pageNum": pageNum,  # 当前页
        "total": total,  # 总数
    }

    _params = {
        "orderId": orderId,  # 订单主单Id
        "userId": userId,  # 用户ID
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/order/finish")
def order_order_finish(orderId=None, headers=None, **kwargs):
    """
    订单提车-Y
    up_time=1675752665

    params: orderId : string : 主订单ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0.失败 1.成功
    params: msg : string : 
    params: data : object : 
    """
    _method = "POST"
    _url = "/order/order/finish"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "orderId": orderId,  # 主订单ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/order/refundReject")
def order_order_refundreject(orderId=None, headers=None, **kwargs):
    """
    订单退款驳回-Y
    up_time=1675395220

    params: orderId : string : 主订单ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0.失败 1.成功
    params: msg : string : 
    params: data : object : 
    """
    _method = "POST"
    _url = "/order/order/refundReject"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "orderId": orderId,  # 主订单ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


