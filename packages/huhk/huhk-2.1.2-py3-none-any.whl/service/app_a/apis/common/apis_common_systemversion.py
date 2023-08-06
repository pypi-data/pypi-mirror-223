import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/common/systemversion/save")
def common_systemversion_save(remark=None, content=None, downloadUrl=None, force=None, size=None, publishStatus=None, version=None, versionId=None, classify=None, name=None, headers=None, **kwargs):
    """
    保存版本信息-Y
    up_time=1675326010

    params: version : string : 版本号
    params: name : string : 版本名称
    params: content : string : 更新内容
    params: remark : string : 备注
    params: classify : string :  Android或IOS
    params: force : string : 强制更新0.否1.是
    params: downloadUrl : string : 下载路径
    params: size : string : 大小
    params: versionId : number : 主键，更新传，新增不传
    params: publishStatus : number : 0. 未发布 1.已发布
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/common/systemversion/save"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "version": version,  # 版本号
        "name": name,  # 版本名称
        "content": content,  # 更新内容
        "remark": remark,  # 备注
        "classify": classify,  #  Android或IOS
        "force": force,  # 强制更新0.否1.是
        "downloadUrl": downloadUrl,  # 下载路径
        "size": size,  # 大小
        "versionId": versionId,  # 主键，更新传，新增不传
        "publishStatus": publishStatus,  # 0. 未发布 1.已发布
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/common/systemversion/page")
def common_systemversion_page( headers=None, **kwargs):
    """
    查询版本信息-Y
    up_time=1675325747

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
              countId : number : 
              maxLimit : number : 
              pages : number : 
    """
    _method = "GET"
    _url = "/common/systemversion/page"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


