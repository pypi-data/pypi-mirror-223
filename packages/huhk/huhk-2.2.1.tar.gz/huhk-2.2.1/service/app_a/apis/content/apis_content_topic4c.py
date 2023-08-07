import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/topic4C/del")
def content_topic4c_del(topicId=None, headers=None, **kwargs):
    """
    话题-删除话题
    up_time=1675133827

    params: topicId : string : 话题主键
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/topic4C/del"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "topicId": topicId,  # 话题主键
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/topic4C/getContentList")
def content_topic4c_getcontentlist(topicId=None, current=None, size=None, headers=None, **kwargs):
    """
    话题-获取动态关联列表-Y
    up_time=1675653387

    params: topicId :  : 话题主键
    params: size :  : 每页数据数
    params: current :  : 当前页
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : array : 
              contentId : string : 内容主键
              topFlag : number : 是否置顶
              createTime : string : 创建时间
              createName : string : 发布人
              userType : number : 用户类型1：潜在客户2：内部用户3：虚拟用户4：保有客户
              mobile : string : 手机号
              topicTitle : string : 话题标题
              contentDesc : string : 动态内容
              contentImg : string : 动态图片
              contentStatus : number : 动态状态
    """
    _method = "GET"
    _url = "/content/topic4C/getContentList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "topicId": topicId,  # 话题主键
        "size": size,  # 每页数据数
        "current": current,  # 当前页
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/topic4C/list")
def content_topic4c_list(createBy=None, topicId=None, current=None, keyWord=None, startTime=None, endTime=None, size=None, headers=None, **kwargs):
    """
    话题-搜索话题列表
    up_time=1675133829

    params: topicId :  : 话题主键
    params: createBy :  : 发布人主键
    params: keyWord :  : 话题关键字
    params: startTime :  : 搜索开始时间
    params: endTime :  : 搜索结束时间
    params: size :  : 每页数量数
    params: current :  : 当前页
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : array : 
              topicId : string : 话题主键
              topFlag : number : 是否置顶1：是0：否
              createTime : string : 创建时间
              publishTime : string : 发布时间
              createName : string : 发布人
              avatarUrl : string : 发布人头像
              topicType : number : 1:动态（目前只有动态）
              userType : number : 发布人类型1：潜在客户2：内部用户3：虚拟用户4：保有客户
              mobile : string : 手机号
              topicTitle : string : 话题标题
              contentCount : number : 动态关联数量
              topicContent : string : 话题内容，描述
    """
    _method = "GET"
    _url = "/content/topic4C/list"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "topicId": topicId,  # 话题主键
        "createBy": createBy,  # 发布人主键
        "keyWord": keyWord,  # 话题关键字
        "startTime": startTime,  # 搜索开始时间
        "endTime": endTime,  # 搜索结束时间
        "size": size,  # 每页数量数
        "current": current,  # 当前页
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/topic4C/insert")
def content_topic4c_insert(topicId=None, author=None, topicTitle=None, headers=None, **kwargs):
    """
    话题-新增话题
    up_time=1675133829

    params: topicId : string : 话题主键
    params: topicTitle : string : 话题
    params: author : number : 话题作者
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/topic4C/insert"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "topicId": topicId,  # 话题主键
        "topicTitle": topicTitle,  # 话题
        "author": author,  # 话题作者
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/topic4C/top")
def content_topic4c_top(topicId=None, type=None, headers=None, **kwargs):
    """
    话题-置顶
    up_time=1675133829

    params: topicId : string : 话题主键
    params: type : string : 操作类型1：置顶2：取消置顶
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/topic4C/top"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "topicId": topicId,  # 话题主键
        "type": type,  # 操作类型1：置顶2：取消置顶
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


