import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/noticeManager/page")
def content_noticemanager_page( headers=None, **kwargs):
    """
    系统通知列表查询接口-Y
    up_time=1675652796

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
              countId : null : 
              maxLimit : null : 
              pages : number : 
    """
    _method = "GET"
    _url = "/content/noticeManager/page"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/noticeManager/getNoticeParamsList/")
def content_noticemanager_getnoticeparamslist_(templateType=None, messageId=None, headers=None, **kwargs):
    """
    获取系统通知详情
    up_time=1675133819

    params: messageId :  : 
    params: templateType :  : 模板编码
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
              countId : null : 
              maxLimit : null : 
              pages : number : 
    """
    _method = "GET"
    _url = "/content/noticeManager/getNoticeParamsList/{messageId}"
    _url = get_url(_url, locals())

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "templateType": templateType,  # 模板编码
    }

    _params = {
        "messageId": messageId,
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/noticeManager/noticeParamsUpdate")
def content_noticemanager_noticeparamsupdate(templateType=None, templateName=None, templateContent=None, headers=None, **kwargs):
    """
    系统通知变量编辑-Y
    up_time=1675652880

    params: templateType : string : 模板类型
    params: templateName : string : 模板名称（标题）
    params: templateContent : string : 模板内容
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/noticeManager/noticeParamsUpdate"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "templateType": templateType,  # 模板类型
        "templateName": templateName,  # 模板名称（标题）
        "templateContent": templateContent,  # 模板内容
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


