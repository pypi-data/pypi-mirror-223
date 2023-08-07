import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/messageManager/page")
def content_messagemanager_page(content=None, userId=None, authId=None, pEndTime=None, messageId=None, cStartTime=None, cEndTime=None, beginTime=None, status=None, pStartTime=None, endTime=None, headers=None, **kwargs):
    """
    消息列表查询接口-Y
    up_time=1675651897

    params: messageId :  : 
    params: userId :  : 
    params: content :  : 
    params: beginTime :  : 前端日期后面必须要追加 00:00:00
    params: endTime :  : 前端日期后面必须要追加 23:59:59
    params: authId :  : 
    params: status :  : -1.结束 0.待审核 1.审核通过 2.审核未通过 3.草稿  4.未发布 5.已发布 6.已撤销 7.已归档 
    params: pStartTime :  : 
    params: pEndTime :  : 
    params: cStartTime :  : 
    params: cEndTime :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : object : 
              records : array : 
              total : number : 总数量
              size : number : 页码大小
              current : number : 当前页码
              pages : number : 总页数
    """
    _method = "GET"
    _url = "/content/messageManager/page"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "messageId": messageId,
        "userId": userId,
        "content": content,
        "beginTime": beginTime,  # 前端日期后面必须要追加 00:00:00
        "endTime": endTime,  # 前端日期后面必须要追加 23:59:59
        "authId": authId,
        "status": status,  # -1.结束 0.待审核 1.审核通过 2.审核未通过 3.草稿  4.未发布 5.已发布 6.已撤销 7.已归档 
        "pStartTime": pStartTime,
        "pEndTime": pEndTime,
        "cStartTime": cStartTime,
        "cEndTime": cEndTime,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/messageManager/getMessageInfo/")
def content_messagemanager_getmessageinfo_(messageId=None, headers=None, **kwargs):
    """
    获取消息详情-Y
    up_time=1675652084

    params: messageId :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              activityId : string : 活动主键
              createTime : string : 创建时间
              createBy : string : 创建人（发布者/作者）
              createByName : string : 创建人（发布者/作者）
              mobile : string : 手机号
              avatar : string : 头像
              username : string : 用户名称
              userType : string : 用户类型 1:内部用户 2:虚拟用户
              activityPicUrl : string : 活动封面图
              title : string : 标题
              joinCnt : string : 参加数量
              activityJoinList : array : 活动参与人数数据集合
    """
    _method = "GET"
    _url = "/content/messageManager/getMessageInfo/{messageId}"
    _url = get_url(_url, locals())

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
        "messageId": messageId,
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/messageManager/messageTop")
def content_messagemanager_messagetop(messageIds=None, topFlag=None, headers=None, **kwargs):
    """
    消息置顶/取消置顶-Y
    up_time=1675652320

    params: messageIds : text : 消息ids集合
    params: topFlag : text : 消息置顶标识 0-置顶 1-不置顶
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/messageManager/messageTop"

    _headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    _headers.update({"headers": headers})

    _data = {
        "messageIds": messageIds,  # 消息ids集合
        "topFlag": topFlag,  # 消息置顶标识 0-置顶 1-不置顶
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/messageManager/insert")
def content_messagemanager_insert(content=None, checkStatus=None, publishType=None, messageId=None, checkPublish=None, publishTime=None, param=None, sendScope=None, imageUrl=None, type=None, sourceType=None, headers=None, **kwargs):
    """
    消息新增接口-Y
    up_time=1675652341

    params: messageId : text : 
    params: type : text : 此处传1
    params: content : text : 
    params: imageUrl : text : 
    params: sourceType : text : 此处传1
    params: param : text : 
    params: sendScope : text : 
    params: checkStatus : text : 
    params: checkPublish : text : 
    params: publishType : text : 
    params: publishTime : text : 
    params: headers : 请求头
    ====================返回======================
    """
    _method = "POST"
    _url = "/content/messageManager/insert"

    _headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    _headers.update({"headers": headers})

    _data = {
        "messageId": messageId,
        "type": type,  # 此处传1
        "content": content,
        "imageUrl": imageUrl,
        "sourceType": sourceType,  # 此处传1
        "param": param,
        "sendScope": sendScope,
        "checkStatus": checkStatus,
        "checkPublish": checkPublish,
        "publishType": publishType,
        "publishTime": publishTime,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/messageManager/update")
def content_messagemanager_update(content=None, checkStatus=None, messageId=None, checkPublish=None, userMobiles=None, param=None, sendScope=None, imageUrl=None, type=None, sourceType=None, headers=None, **kwargs):
    """
    消息编辑接口-Y
    up_time=1675652502

    params: messageId :  : 
    params: type :  : 此处传1
    params: content :  : 
    params: imageUrl :  : 
    params: sourceType :  : 此处传1
    params: param :  : 
    params: sendScope :  : 
    params: checkStatus :  : 
    params: checkPublish :  : 
    params: userMobiles :  : ["131xxxx1234","132xxxx1234"]
    params: headers : 请求头
    ====================返回======================
    """
    _method = "POST"
    _url = "/content/messageManager/update"

    _headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    _headers.update({"headers": headers})

    _data = {
        "messageId": messageId,
        "type": type,  # 此处传1
        "content": content,
        "imageUrl": imageUrl,
        "sourceType": sourceType,  # 此处传1
        "param": param,
        "sendScope": sendScope,
        "checkStatus": checkStatus,
        "checkPublish": checkPublish,
        "userMobiles": userMobiles,  # ["131xxxx1234","132xxxx1234"]
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/messageManager/publishUpdate")
def content_messagemanager_publishupdate(messageIds=None, publishStatus=None, headers=None, **kwargs):
    """
    消息发布状态修改-Y
    up_time=1675652643

    params: messageIds : text : 
    params: publishStatus : text : 
    params: headers : 请求头
    ====================返回======================
    """
    _method = "POST"
    _url = "/content/messageManager/publishUpdate"

    _headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    _headers.update({"headers": headers})

    _data = {
        "messageIds": messageIds,
        "publishStatus": publishStatus,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/messageManager/statusUpdate")
def content_messagemanager_statusupdate(messageIds=None, checkStatus=None, headers=None, **kwargs):
    """
    消息审核状态修改
    up_time=1675133819

    params: messageIds : text : 
    params: checkStatus : text : 
    params: headers : 请求头
    ====================返回======================
    """
    _method = "POST"
    _url = "/content/messageManager/statusUpdate"

    _headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    _headers.update({"headers": headers})

    _data = {
        "messageIds": messageIds,
        "checkStatus": checkStatus,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


