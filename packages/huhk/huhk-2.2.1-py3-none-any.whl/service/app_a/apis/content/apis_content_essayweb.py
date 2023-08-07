import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/essayweb/add")
def content_essayweb_add(essPicUrl=None, content=None, publishType=None, title=None, author=None, status=None, publishTime=None, essayId=None, publishChannel=None, headers=None, **kwargs):
    """
    专题-后台官网专题新建文章-Y
    up_time=1675737086

    params: essayId : string : 文章主键
    params: title : string : 文章标题
    params: author : string : 作者
    params: publishType : string : 发布类型1：立即发布2：定时发布
    params: publishTime : string : 定时发布时间
    params: essPicUrl : string : 文章封面
    params: publishChannel : string : 发布渠道
    params: content : string : 文章正文富文本
    params: status : string : 保存时传1，提交审核时传2
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/essayweb/add"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "essayId": essayId,  # 文章主键
        "title": title,  # 文章标题
        "author": author,  # 作者
        "publishType": publishType,  # 发布类型1：立即发布2：定时发布
        "publishTime": publishTime,  # 定时发布时间
        "essPicUrl": essPicUrl,  # 文章封面
        "publishChannel": publishChannel,  # 发布渠道
        "content": content,  # 文章正文富文本
        "status": status,  # 保存时传1，提交审核时传2
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/essayweb/searchByKey")
def content_essayweb_searchbykey(key=None, current=None, size=None, headers=None, **kwargs):
    """
    专题-后台官网文章关键词搜索-Y
    up_time=1675737282

    params: current :  : 当前页
    params: size :  : 每页条数
    params: key :  : 关键词
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/content/essayweb/searchByKey"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,  # 当前页
        "size": size,  # 每页条数
        "key": key,  # 关键词
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/essayweb/delete/")
def content_essayweb_delete_(essayId=None, headers=None, **kwargs):
    """
    专题-后台官网文章删除-Y
    up_time=1675737243

    params: essayId :  : 文章id
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0 成功 1失败 
    params: msg : string : 
    params: data : null : 
    """
    _method = "POST"
    _url = "/content/essayweb/delete/{essayId}"
    _url = get_url(_url, locals())

    _headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
        "essayId": essayId,  # 文章id
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/essayweb/getById")
def content_essayweb_getbyid(essayId=None, subjectId=None, headers=None, **kwargs):
    """
    新闻中心查看文章详情-Y
    up_time=1675737040

    params: essayId :  : 文章主键
    params: subjectId :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              code : number : 
              msg : string : 
              data : object : 
    """
    _method = "GET"
    _url = "/content/essayweb/getById"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "essayId": essayId,  # 文章主键
        "subjectId": subjectId,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


