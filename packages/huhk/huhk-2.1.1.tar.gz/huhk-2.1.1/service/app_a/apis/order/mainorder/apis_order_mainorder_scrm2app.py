import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/order/mainOrder/scrm2app/refundAuditNotice")
def order_mainorder_scrm2app_refundauditnotice(orderMainId=None, orderSubId=None, status=None, headers=None, **kwargs):
    """
    订单管理-订单退款-Y
    up_time=1675660605

    params: orderMainId : string : 
    params: orderSubId : string : 
    params: status : integer : 
    params: headers : 请求头
    ====================返回======================
    params: code : integer : 0失败 1成功
    params: msg : string : 
    params: data : object : 
    """
    _method = "POST"
    _url = "/order/mainOrder/scrm2app/refundAuditNotice"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "orderMainId": orderMainId,
        "orderSubId": orderSubId,
        "status": status,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


