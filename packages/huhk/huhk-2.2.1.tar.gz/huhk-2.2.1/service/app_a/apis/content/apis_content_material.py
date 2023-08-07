import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/material/delGroup")
def content_material_delgroup(groupId=None, headers=None, **kwargs):
    """
    素材-删除分组-Y
    up_time=1675651277

    params: groupId : number : 素材分组主键
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/material/delGroup"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "groupId": groupId,  # 素材分组主键
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/material/delMaterial")
def content_material_delmaterial( headers=None, **kwargs):
    """
    素材-批量删除
    up_time=1675133826

    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/material/delMaterial"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/material/updateGroup")
def content_material_updategroup(groupName=None, groupId=None, headers=None, **kwargs):
    """
    素材-更新素材分组-Y
    up_time=1675651159

    params: groupName : string : 分组名称
    params: groupId : number : 分组主键
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/material/updateGroup"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "groupName": groupName,  # 分组名称
        "groupId": groupId,  # 分组主键
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/material/getMaterialList")
def content_material_getmateriallist(current=None, groupId=None, size=None, headers=None, **kwargs):
    """
    素材-根据素材组获取素材列表
    up_time=1675133826

    params: groupId :  : 分组主键
    params: size :  : 每页数据数
    params: current :  : 当前页
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
    _url = "/content/material/getMaterialList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "groupId": groupId,  # 分组主键
        "size": size,  # 每页数据数
        "current": current,  # 当前页
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/material/addGroup")
def content_material_addgroup(groupName=None, headers=None, **kwargs):
    """
    素材-添加素材分组-Y
    up_time=1675651559

    params: groupName : string : 分组名称
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/material/addGroup"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "groupName": groupName,  # 分组名称
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/material/addMaterial")
def content_material_addmaterial(file=None, groupId=None, headers=None, **kwargs):
    """
    素材-素材上传
    up_time=1675133827

    params: file : file : 上传文件
    params: groupId : text : 所属分组主键
    params: headers : 请求头
    ====================返回======================
    params: url : string : 素材路径
    """
    _method = "POST"
    _url = "/content/material/addMaterial"

    _headers = {
        "Content-Type": "multipart/form-data",
    }
    _headers.update({"headers": headers})

    _data = {
        "file": file,  # 上传文件
        "groupId": groupId,  # 所属分组主键
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/material/getGroupList")
def content_material_getgrouplist(groupName=None, headers=None, **kwargs):
    """
    素材-素材组列表-Y
    up_time=1675651014

    params: groupName :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              records : array : 
              total : number : 数据总数
              size : number : 每页数据数
              current : number : 当前页数
              orders : array : 
              optimizeCountSql : boolean : 
              searchCount : boolean : 
              countId : null : 
              maxLimit : null : 
              pages : number : 
    """
    _method = "GET"
    _url = "/content/material/getGroupList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "groupName": groupName,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


