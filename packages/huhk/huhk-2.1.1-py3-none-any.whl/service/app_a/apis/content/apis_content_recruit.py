import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/recruit/save")
def content_recruit_save(fileName=None, fileUrl=None, headers=None, **kwargs):
    """
    招聘信息保存-Y
    up_time=1675740268

    params: fileName : string : 文件名
    params: fileUrl : string : 文件url
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0:成功   1:失败
    params: msg : string : 信息
    params: data : boolean : true成功;  false失败
    """
    _method = "POST"
    _url = "/content/recruit/save"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "fileName": fileName,  # 文件名
        "fileUrl": fileUrl,  # 文件url
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/recruit/detail")
def content_recruit_detail( headers=None, **kwargs):
    """
    招聘信息查询-Y
    up_time=1675740254

    params: headers : 请求头
    ====================返回======================
    params: code : number : 0:成功  1:失败
    params: msg : string : 信息
    params: data : object : 
              recruitId : string : 
              fileName : string : 文件名
              fileUrl : string : 文件url
              createTime : string : 
              createBy : string : 
              updateTime : string : 
              updateBy : string : 
              delFlag : number : 
    """
    _method = "GET"
    _url = "/content/recruit/detail"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


