import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/commonquestion/updateStatus")
def content_commonquestion_updatestatus(essayId=None, status=None, headers=None, **kwargs):
    """
    常见问题-上下架-Y
    up_time=1675681221

    params: essayId :  : 主键id
    params: status : string : 上架2 下架3
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0 成功 1失败
    params: msg : string : 
    params: data : string : 
    """
    _method = "POST"
    _url = "/content/commonquestion/updateStatus"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "essayId": essayId,  # 主键id
        "status": status,  # 上架2 下架3
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/commonquestion/update")
def content_commonquestion_update(content=None, essayId=None, title=None, headers=None, **kwargs):
    """
    常见问题-修改-Y
    up_time=1675681308

    params: essayId :  : 主键id
    params: title : string : 标题
    params: content : string : 内容
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0 成功 1失败
    params: msg : string : 
    params: data : string : 
    """
    _method = "POST"
    _url = "/content/commonquestion/update"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "essayId": essayId,  # 主键id
        "title": title,  # 标题
        "content": content,  # 内容
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/commonquestion/updateRank")
def content_commonquestion_updaterank(essayId=None, rank=None, headers=None, **kwargs):
    """
    常见问题-修改权重-Y
    up_time=1675681234

    params: essayId :  : 主键id
    params: rank : string : 权重
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0 成功 1失败
    params: msg : string : 
    params: data : string : 
    """
    _method = "POST"
    _url = "/content/commonquestion/updateRank"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "essayId": essayId,  # 主键id
        "rank": rank,  # 权重
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/commonquestion/delete")
def content_commonquestion_delete(essayId=None, headers=None, **kwargs):
    """
    常见问题-删除-Y
    up_time=1675681073

    params: essayId :  : 主键id
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0 成功 1失败 
    params: msg : string : 
    params: data : string : 
    """
    _method = "POST"
    _url = "/content/commonquestion/delete"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "essayId": essayId,  # 主键id
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/commonquestion/list")
def content_commonquestion_list(current=None, size=None, headers=None, **kwargs):
    """
    常见问题-后台列表-Y
    up_time=1675681018

    params: current :  : 当前页数
    params: size :  : 每页个数
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              records : array : 
              total : number : 
              size : number : 
              current : number : 
              pages : number : 
    """
    _method = "GET"
    _url = "/content/commonquestion/list"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,  # 当前页数
        "size": size,  # 每页个数
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/commonquestion/publishList")
def content_commonquestion_publishlist(current=None, size=None, headers=None, **kwargs):
    """
    常见问题-已发布列表-Y
    up_time=1675681033

    params: current :  : 当前页数
    params: size :  : 每页数量
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              records : array : 
              total : number : 
              size : number : 
              current : number : 
              pages : number : 
    """
    _method = "GET"
    _url = "/content/commonquestion/publishList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,  # 当前页数
        "size": size,  # 每页数量
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/commonquestion/add")
def content_commonquestion_add(content=None, essayId=None, title=None, headers=None, **kwargs):
    """
    常见问题-新增-Y
    up_time=1675681275

    params: essayId :  : 主键id
    params: title : string : 标题
    params: content : string : 内容
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0 成功 1失败
    params: msg : string : 
    params: data : string : 
    """
    _method = "POST"
    _url = "/content/commonquestion/add"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "essayId": essayId,  # 主键id
        "title": title,  # 标题
        "content": content,  # 内容
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/commonquestion/createId")
def content_commonquestion_createid( headers=None, **kwargs):
    """
    常见问题-生成id-Y
    up_time=1675681168

    params: headers : 请求头
    ====================返回======================
    params: code : number : 0 成功 1失败
    params: msg : string : 
    params: data : string : 生成的id
    """
    _method = "GET"
    _url = "/content/commonquestion/createId"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/commonquestion/info")
def content_commonquestion_info(essayId=None, headers=None, **kwargs):
    """
    常见问题-详情-Y
    up_time=1675681050

    params: essayId :  : 主键id
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              essayId : string : 主键id
              title : string : 标题
              content : string : 内容
              status : number : 状态1：未上架 2：已上架3：已下架 4：已删除
              updateTime : string : 编辑时间
              updateBy : null : 编辑人
              updateByName : null : 编辑人姓名
              publishTime : string : 发布时间
              rank : number : 权重
              delFlag : number :  0 正常 1删除
    """
    _method = "GET"
    _url = "/content/commonquestion/info"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "essayId": essayId,  # 主键id
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


