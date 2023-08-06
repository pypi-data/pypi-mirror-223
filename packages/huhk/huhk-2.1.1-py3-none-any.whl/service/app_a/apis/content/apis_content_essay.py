import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/essay/delete/")
def content_essay_delete_(essayId=None, headers=None, **kwargs):
    """
    专题-后台APP专题文章删除-Y
    up_time=1675736702

    params: essayId :  : 文章id
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0 成功 1失败
    params: msg : string : 
    params: data : null : 
    """
    _method = "POST"
    _url = "/content/essay/delete/{essayId}"
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


@allure.step(title="调接口：/content/essay/searchByKey")
def content_essay_searchbykey(current=None, Key=None, size=None, headers=None, **kwargs):
    """
    专题-后台App文章关键词搜索-Y
    up_time=1675736722

    params: Key :  : 关键词
    params: size :  : 条数
    params: current :  : 当前页
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/content/essay/searchByKey"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "Key": Key,  # 关键词
        "size": size,  # 条数
        "current": current,  # 当前页
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/essay/checkList")
def content_essay_checklist(StatusSortType=None, current=None, author=None, status=None, essayId=None, keyWord=None, subjectId=None, recommend=None, startTime=None, endTime=None, CreateTimeSortType=None, size=None, PublishTimeSortType=None, headers=None, **kwargs):
    """
    后台管理-内容审核列表1030-Y
    up_time=1675736061

    params: essayId :  : 文章主键
    params: keyWord :  : 文章搜索关键字
    params: author :  : 作者
    params: startTime :  : 搜索开始时间
    params: endTime :  : 搜索结束时间
    params: subjectId :  : 专题主键
    params: status :  : 文章状态1：待上架2：已上架3：已下架4：已删除 5 待审核 6 审核不通过 7草稿
    params: size :  : 每页条数
    params: current :  : 当前页数
    params: recommend :  : 是否推荐 1：推荐页0：非推荐页
    params: PublishTimeSortType :  : 发布时间排序方式 默认倒序，正序  ASC 倒序 DESC
    params: CreateTimeSortType :  : 创建时间排序方式 默认倒序，  正序  ASC 倒序 DESC
    params: StatusSortType :  : 状态排序方式 默认倒序，  正序  ASC 倒序 DESC
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
    _url = "/content/essay/checkList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "essayId": essayId,  # 文章主键
        "keyWord": keyWord,  # 文章搜索关键字
        "author": author,  # 作者
        "startTime": startTime,  # 搜索开始时间
        "endTime": endTime,  # 搜索结束时间
        "subjectId": subjectId,  # 专题主键
        "status": status,  # 文章状态1：待上架2：已上架3：已下架4：已删除 5 待审核 6 审核不通过 7草稿
        "size": size,  # 每页条数
        "current": current,  # 当前页数
        "recommend": recommend,  # 是否推荐 1：推荐页0：非推荐页
        "PublishTimeSortType": PublishTimeSortType,  # 发布时间排序方式 默认倒序，正序  ASC 倒序 DESC
        "CreateTimeSortType": CreateTimeSortType,  # 创建时间排序方式 默认倒序，  正序  ASC 倒序 DESC
        "StatusSortType": StatusSortType,  # 状态排序方式 默认倒序，  正序  ASC 倒序 DESC
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/essay/list")
def content_essay_list(StatusSortType=None, current=None, author=None, status=None, essayId=None, keyWord=None, subjectId=None, recommend=None, startTime=None, endTime=None, CreateTimeSortType=None, size=None, PublishTimeSortType=None, headers=None, **kwargs):
    """
    后台管理-内容管理列表1030-Y
    up_time=1675736044

    params: essayId :  : 文章主键
    params: keyWord :  : 文章搜索关键字
    params: author :  : 作者
    params: startTime :  : 搜索开始时间
    params: endTime :  : 搜索结束时间
    params: subjectId :  : 专题主键
    params: status :  : 文章状态1：待上架2：已上架3：已下架4：已删除 5 待审核 6 审核不通过 7草稿
    params: size :  : 每页条数
    params: current :  : 当前页数
    params: recommend :  : 是否推荐 1：推荐页0：非推荐页
    params: PublishTimeSortType :  : 发布时间排序方式 默认倒序，正序  ASC 倒序 DESC
    params: CreateTimeSortType :  : 创建时间排序方式 默认倒序，  正序  ASC 倒序 DESC
    params: StatusSortType :  : 状态排序方式 默认倒序，  正序  ASC 倒序 DESC
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
    _url = "/content/essay/list"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "essayId": essayId,  # 文章主键
        "keyWord": keyWord,  # 文章搜索关键字
        "author": author,  # 作者
        "startTime": startTime,  # 搜索开始时间
        "endTime": endTime,  # 搜索结束时间
        "subjectId": subjectId,  # 专题主键
        "status": status,  # 文章状态1：待上架2：已上架3：已下架4：已删除 5 待审核 6 审核不通过 7草稿
        "size": size,  # 每页条数
        "current": current,  # 当前页数
        "recommend": recommend,  # 是否推荐 1：推荐页0：非推荐页
        "PublishTimeSortType": PublishTimeSortType,  # 发布时间排序方式 默认倒序，正序  ASC 倒序 DESC
        "CreateTimeSortType": CreateTimeSortType,  # 创建时间排序方式 默认倒序，  正序  ASC 倒序 DESC
        "StatusSortType": StatusSortType,  # 状态排序方式 默认倒序，  正序  ASC 倒序 DESC
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/essay/add")
def content_essay_add(content=None, essPicUrl=None, publishType=None, title=None, author=None, essayType=None, videoUrl=None, status=None, publishTime=None, essayId=None, subjectId=None, recommend=None, headers=None, **kwargs):
    """
    后台管理-新建&修改内容1030-Y
    up_time=1675736497

    params: essayId : string : 文章主键
    params: title : string : 标题
    params: author : string : 作者
    params: publishType : number : 发布类型1：立即发布2：定时发布
    params: publishTime : string : 发布时间
    params: content : string : 富文本内容
    params: status : string : 状态 新增状态为待审核 1：待上架2：已上架 3 ：已下架4：已删除 5待审核 6 审核不通过 7 草稿
    params: essayType : string : 文章类型1：图文2：视频
    params: subjectId : array : 专题主键
              type : string : None
    params: recommend : number : 是否推荐 1：推荐页0：非推荐页
    params: essPicUrl : string : 封面
    params: videoUrl : string : 视频路径
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/essay/add"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "essayId": essayId,  # 文章主键
        "title": title,  # 标题
        "author": author,  # 作者
        "publishType": publishType,  # 发布类型1：立即发布2：定时发布
        "publishTime": publishTime,  # 发布时间
        "content": content,  # 富文本内容
        "status": status,  # 状态 新增状态为待审核 1：待上架2：已上架 3 ：已下架4：已删除 5待审核 6 审核不通过 7 草稿
        "essayType": essayType,  # 文章类型1：图文2：视频
        "subjectId": subjectId,  # 专题主键
        "recommend": recommend,  # 是否推荐 1：推荐页0：非推荐页
        "essPicUrl": essPicUrl,  # 封面
        "videoUrl": videoUrl,  # 视频路径
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/essay/createId")
def content_essay_createid( headers=None, **kwargs):
    """
    文章-生成文章主键-Y
    up_time=1675736244

    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : string : 主键
    """
    _method = "GET"
    _url = "/content/essay/createId"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/essay/getById")
def content_essay_getbyid(essayId=None, headers=None, **kwargs):
    """
    后台管理-内容详情1030-Y
    up_time=1675736219

    params: essayId :  : 文章主键
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : object : 
              essayId : string : 文章主键
              title : string : 文章标题
              author : number : 作者主键
              authorName : string : 作者名称
              authorImg : string : 作者头像
              essPicUrl : string : 文章封面
              content : string : 文章正文
              status : number : 文章当前状态
    """
    _method = "GET"
    _url = "/content/essay/getById"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "essayId": essayId,  # 文章主键
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/essay/updateStatus")
def content_essay_updatestatus( headers=None, **kwargs):
    """
    后台管理-内容审核1030-Y
    up_time=1675736685

    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/essay/updateStatus"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/essay/getCommentList")
def content_essay_getcommentlist(checkedStatus=None, parentId=None, current=None, commentId=None, essayId=None, keyWord=None, startTime=None, endTime=None, size=None, headers=None, **kwargs):
    """
    后台管理-评论信息1030-Y
    up_time=1675736123

    params: essayId :  : 文章主键
    params: keyWord :  : 关键词
    params: checkedStatus :  : 审核状态 审核状态 0待审核 1.已上架 2.审核未通过3：已下架 5已删除
    params: startTime :  : 开始时间
    params: endTime :  : 结束时间
    params: commentId :  : 评论id
    params: parentId :  : 父级id
    params: size :  : 每页数量
    params: current :  : 当前页
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              ysj : number : 已上架评论数量
              dsh : number : 待审核评论数量
              ysc : number : 已删除评论数量
              yxj : number : 已下架评论数量
              page : object : 
              shbg : number : 审核不过数量
    """
    _method = "GET"
    _url = "/content/essay/getCommentList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "essayId": essayId,  # 文章主键
        "keyWord": keyWord,  # 关键词
        "checkedStatus": checkedStatus,  # 审核状态 审核状态 0待审核 1.已上架 2.审核未通过3：已下架 5已删除
        "startTime": startTime,  # 开始时间
        "endTime": endTime,  # 结束时间
        "commentId": commentId,  # 评论id
        "parentId": parentId,  # 父级id
        "size": size,  # 每页数量
        "current": current,  # 当前页
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


