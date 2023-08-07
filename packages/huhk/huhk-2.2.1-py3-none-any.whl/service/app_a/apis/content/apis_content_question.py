import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/question/answerQuestion")
def content_question_answerquestion(questionId=None, author=None, answerContent=None, headers=None, **kwargs):
    """
    问答-回复问题-Y
    up_time=1675680341

    params: questionId : string : 问题主键
    params: answerContent : string : 回答内容
    params: author : number : 作者
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/question/answerQuestion"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "questionId": questionId,  # 问题主键
        "answerContent": answerContent,  # 回答内容
        "author": author,  # 作者
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/question/revoke")
def content_question_revoke(questionId=None, operaType=None, headers=None, **kwargs):
    """
    问答-回答撤回归档-Y
    up_time=1675740174

    params: operaType : string : 操作类型3：撤回4：归档
    params: questionId : string : 回复主键
    params: headers : 请求头
    ====================返回======================
    """
    _method = "POST"
    _url = "/content/question/revoke"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "operaType": operaType,  # 操作类型3：撤回4：归档
        "questionId": questionId,  # 回复主键
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/question/getManegeQuestionList")
def content_question_getmanegequestionlist(current=None, status=None, mobile=None, keyWord=None, startTime=None, endTime=None, size=None, headers=None, **kwargs):
    """
    问答-搜索问题列表-Y
    up_time=1675740163

    params: keyWord :  : 关键字
    params: mobile :  : 发布人手机号
    params: startTime :  : 搜索起始时间
    params: endTime :  : 搜索结束时间
    params: status :  : 问答状态1：已回复、0：待回复、3：已撤回、4：已归档
    params: size :  : 每页数据量
    params: current :  : 页数
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              records : array : 
              total : number : 数量
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
    _url = "/content/question/getManegeQuestionList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "keyWord": keyWord,  # 关键字
        "mobile": mobile,  # 发布人手机号
        "startTime": startTime,  # 搜索起始时间
        "endTime": endTime,  # 搜索结束时间
        "status": status,  # 问答状态1：已回复、0：待回复、3：已撤回、4：已归档
        "size": size,  # 每页数据量
        "current": current,  # 页数
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/question/getById")
def content_question_getbyid(questionId=None, headers=None, **kwargs):
    """
    问答-获取问题详情页面-Y
    up_time=1675740037

    params: questionId :  : 问题主键
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              questionId : string : 问题id
              content : string : 内容
              classifyId : string : 分类id
              chackStatus : number : 状态  0：待回复 1.已回复 3.已撤回 4.已归档
              ansCnt : string : 回答数量
              reason : null : 原因
              checkTime : null : 审核时间
              checkBy : string : 审核人
              delFlag : number : 是否删除  1.已删除
              createTime : string : 创建时间
              createBy : string : 创建人id
              updateTime : null : 修改时间
              updateBy : null : 修改人id
              picUrls : array : 图片集合
              userType : number : 用户类型
              classifyName : string : 分类名称（页面显示）
              createAvatarUrl : string : 用户头像
              createName : string : 用户昵称
              answers : array : 回答
              keyWord : null : 
              mobile : string : 用户手机号
              startTime : null : 
              endTime : null : 
              status : null : 
    """
    _method = "GET"
    _url = "/content/question/getById"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "questionId": questionId,  # 问题主键
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


