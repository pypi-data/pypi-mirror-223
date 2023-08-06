import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/safeCode/close")
def content_safecode_close(safeCode=None, headers=None, **kwargs):
    """
    安全码关闭-Y
    up_time=1675748298

    params: safeCode : string : 安全码
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : number : 0: 关闭成功 1:安全码错误
    """
    _method = "POST"
    _url = "/content/safeCode/close"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "safeCode": safeCode,  # 安全码
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/safeCode/add")
def content_safecode_add(safeCode=None, headers=None, **kwargs):
    """
    安全码新增-Y
    up_time=1675748271

    params: safeCode : string : 安全码
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : true成功; false失败
    """
    _method = "POST"
    _url = "/content/safeCode/add"

    _headers = {
        "Content-Type": "application/json",
        "rId": "77289A5EC1EDEB725AB1E7FCE3F8BE514091FEBE44315EC1AF6B410C415CA4E95728211641DC8DF8A7B7A7F18A080583D1531C5CFD08E7CAF62A31E86EAAA1CBF9DFE98543619DE617719D183644CA63661C5BF808740BB5896D90EAE4A8DF81BA090FE05C138F43749CF88F78705E998A8FBACF4236F70FF870F959D667B070C510EB85ED1F3D88C4A2899AB24BC166880055B41EDD9E29D8F19EAD763D3585C6B51D585A8E4DEE6F34847A71A1F65E48576CDADC1F5D5E6D8C249E8405333081C1A3FAF55A0F2CC3EB21F01123873A ",
        "system": "iOS",
        "aId": "77289A5EC1EDEB725AB1E7FCE3F8BE514091FEBE44315EC1AF6B410C415CA4E95728211641DC8DF8A7B7A7F18A080583D1531C5CFD08E7CAF62A31E86EAAA1CBF9DFE98543619DE617719D183644CA63661C5BF808740BB5896D90EAE4A8DF81BA090FE05C138F43749CF88F78705E998A8FBACF4236F70FF870F959D667B070C510EB85ED1F3D88C4A2899AB24BC166880055B41EDD9E29D8F19EAD763D3585C6B51D585A8E4DEE6F34847A71A1F65E48576CDADC1F5D5E6D8C249E8405333081C1A3FAF55A0F2CC3EB21F01123873A ",
    }
    _headers.update({"headers": headers})

    _data = {
        "safeCode": safeCode,  # 安全码
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/safeCode/verify")
def content_safecode_verify(safeCode=None, headers=None, **kwargs):
    """
    安全码校验-Y
    up_time=1675748319

    params: safeCode :  : 安全码
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : number : 0:校验成功 1:安全码错误 2:已锁定
    """
    _method = "GET"
    _url = "/content/safeCode/verify"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "safeCode": safeCode,  # 安全码
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/safeCode/getStatus")
def content_safecode_getstatus( headers=None, **kwargs):
    """
    安全码状态查询-Y
    up_time=1675748015

    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              mobile : string : 手机号
              status : number : 安全码状态(0:未设置 1:已设置)
              isNeedGuide : number : 是否需要指引(0:不需要 1:需要)
    """
    _method = "GET"
    _url = "/content/safeCode/getStatus"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/safeCode/reset")
def content_safecode_reset(safeCode=None, headers=None, **kwargs):
    """
    安全码重置-Y
    up_time=1675748330

    params: safeCode : string : 安全码
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : number : 0:安全码重置成功  1:新密码和旧密码相同 
    """
    _method = "POST"
    _url = "/content/safeCode/reset"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "safeCode": safeCode,  # 安全码
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


