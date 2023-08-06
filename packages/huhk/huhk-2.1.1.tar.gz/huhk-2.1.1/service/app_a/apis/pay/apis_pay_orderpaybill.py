import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/pay/orderpaybill/orderRefund")
def pay_orderpaybill_orderrefund(orderMainId=None, headers=None, **kwargs):
    """
    订单退款接口-Y
    up_time=1675660576

    params: orderMainId :  : 订单id
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : null : 
    """
    _method = "GET"
    _url = "/pay/orderpaybill/orderRefund"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "orderMainId": orderMainId,  # 订单id
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


