import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/comment/updateStatus")
def content_comment_updatestatus(commentId=None, fromStatus=None, toStatus=None, commentType=None, headers=None, **kwargs):
    """
    评论-状态扭转（通用）-Y
    up_time=1675394720

    params: commentId :  : 评论主键
    params: commentType :  : 评论类型1：文章评论2：动态评论	
    params: fromStatus :  : 当前状态
    params: toStatus :  : 扭转状态
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/comment/updateStatus"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "commentId": commentId,  # 评论主键
        "commentType": commentType,  # 评论类型1：文章评论2：动态评论	
        "fromStatus": fromStatus,  # 当前状态
        "toStatus": toStatus,  # 扭转状态
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/comment/downLoad")
def content_comment_download(downloadType=None, nickName=None, status=None, mobile=None, keyWord=None, contentCommentIds=None, startTime=None, endTime=None, EssayCommentIds=None, headers=None, **kwargs):
    """
    评论-评论导出-Y
    up_time=1675649477

    params: mobile :  : 评论用户手机号
    params: nickName :  : 评论昵称
    params: keyWord :  : 搜索关键字
    params: startTime :  : 搜索起始时间
    params: endTime :  : 搜索结束时间
    params: status :  : 状态0.待审核 1.已审核 2.审核未通过3：已发布4：已屏蔽
    params: downloadType :  : 1：根据搜索条件导出2：多选导出
    params: EssayCommentIds :  : 文章评论主键，用英文,隔开
    params: contentCommentIds :  : 动态评论主键，用英文,隔开
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/content/comment/downLoad"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "mobile": mobile,  # 评论用户手机号
        "nickName": nickName,  # 评论昵称
        "keyWord": keyWord,  # 搜索关键字
        "startTime": startTime,  # 搜索起始时间
        "endTime": endTime,  # 搜索结束时间
        "status": status,  # 状态0.待审核 1.已审核 2.审核未通过3：已发布4：已屏蔽
        "downloadType": downloadType,  # 1：根据搜索条件导出2：多选导出
        "EssayCommentIds": EssayCommentIds,  # 文章评论主键，用英文,隔开
        "contentCommentIds": contentCommentIds,  # 动态评论主键，用英文,隔开
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/comment/commentTop")
def content_comment_commenttop(commentId=None, topFlag=None, commentType=None, headers=None, **kwargs):
    """
    评论-评论置顶（通用）-Y
    up_time=1675663979

    params: commentId : string : 评论主键
    params: commentType : number : 评论类型1：文章评论2：动态评论
    params: topFlag : number : 1：置顶0：取消置顶
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/comment/commentTop"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "commentId": commentId,  # 评论主键
        "commentType": commentType,  # 评论类型1：文章评论2：动态评论
        "topFlag": topFlag,  # 1：置顶0：取消置顶
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/comment/list")
def content_comment_list(commentType=None, nickName=None, current=None, checkedStatus=None, mobile=None, keyWord=None, essayId=None, startTime=None, endTime=None, size=None, headers=None, **kwargs):
    """
    后台管理-评论管理列表1030-Y
    up_time=1675394167

    params: nickName :  : 用户昵称 String
    params: keyWord :  : 搜索内容关键字  String
    params: startTime :  : 搜索开始时间 yyyy-MM-dd HH:mm:ss
    params: endTime :  : 搜索结束时间 yyyy-MM-dd HH:mm:ss
    params: size :  : 每页数量数
    params: current :  : 当前页
    params: commentType :  : 评论类型1：文章评论 2：动态 Integer
    params: checkedStatus :  : 审核状态 0待审核 1.已上架 2.审核未通过3：已发布 5已删除 Integer
    params: mobile :  : 电话 string
    params: essayId :  : 文章(资讯)主键 string
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              records : array : 
              total : number : 总页数
              size : number : 每页大小
              current : number : 当前页
              pages : number : 页数
    """
    _method = "GET"
    _url = "/content/comment/list"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "nickName": nickName,  # 用户昵称 String
        "keyWord": keyWord,  # 搜索内容关键字  String
        "startTime": startTime,  # 搜索开始时间 yyyy-MM-dd HH:mm:ss
        "endTime": endTime,  # 搜索结束时间 yyyy-MM-dd HH:mm:ss
        "size": size,  # 每页数量数
        "current": current,  # 当前页
        "commentType": commentType,  # 评论类型1：文章评论 2：动态 Integer
        "checkedStatus": checkedStatus,  # 审核状态 0待审核 1.已上架 2.审核未通过3：已发布 5已删除 Integer
        "mobile": mobile,  # 电话 string
        "essayId": essayId,  # 文章(资讯)主键 string
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/comment/delete")
def content_comment_delete(commentId=None, toStatus=None, commentType=None, headers=None, **kwargs):
    """
    评论-屏蔽评论-Y
    up_time=1675394437

    params: commentId : string : 评论主键
    params: commentType : number : 1：文章评论2：动态评论
    params: toStatus : string : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/comment/delete"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "commentId": commentId,  # 评论主键
        "commentType": commentType,  # 1：文章评论2：动态评论
        "toStatus": toStatus,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


