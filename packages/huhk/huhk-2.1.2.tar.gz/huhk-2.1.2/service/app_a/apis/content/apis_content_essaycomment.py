import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/essaycomment/manageAdd")
def content_essaycomment_manageadd(author=None, essayId=None, parentId=None, content=None, headers=None, **kwargs):
    """
    后台管理-新建评论/回复1030-Y
    up_time=1675735107

    params: essayId : string : 文章id
    params: author : string : 评论人id
    params: content : string : 内容
    params: parentId : string : 所回复评论的id 新建评论不用传 回复要传
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0 成功
    params: msg : string : 
    params: data : null : 
    """
    _method = "POST"
    _url = "/content/essaycomment/manageAdd"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "essayId": essayId,  # 文章id
        "author": author,  # 评论人id
        "content": content,  # 内容
        "parentId": parentId,  # 所回复评论的id 新建评论不用传 回复要传
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


