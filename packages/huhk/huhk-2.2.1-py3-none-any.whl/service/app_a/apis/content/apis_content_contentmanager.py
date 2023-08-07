import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/contentManager/commentList")
def content_contentmanager_commentlist(current=None, size=None, contentId=None, headers=None, **kwargs):
    """
    动态-评论列表-Y
    up_time=1675650512

    params: contentId :  : 动态主键
    params: size :  : 每页数据数
    params: current :  : 当前页
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : array : 
              commentId : string : 评论主键
              topFlag : number : 是否置顶1：是0：否
              checkTime : string : 发布时间
              contentDesc : string : 评论内容
              createName : string : 创建人
              createImg : string : 创建人头像
              mobile : string : 手机号
    """
    _method = "GET"
    _url = "/content/contentManager/commentList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "contentId": contentId,  # 动态主键
        "size": size,  # 每页数据数
        "current": current,  # 当前页
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


