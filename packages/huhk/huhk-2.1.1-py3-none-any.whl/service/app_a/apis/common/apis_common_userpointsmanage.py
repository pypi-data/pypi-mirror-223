import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/common/userPointsManage/userPointsExport")
def common_userpointsmanage_userpointsexport(nickName=None, beginTime=None, mobile=None, logIds=None, endTime=None, headers=None, **kwargs):
    """
    用户积分列表导出-历史接口
    up_time=1676338877

    params: nickName :  : 用户昵称
    params: mobile :  : 用户手机号
    params: beginTime :  : 注册时间查询范围--开始时间
    params: endTime :  : 注册时间查询范围--结束时间
    params: logIds :  : 积分明细Id，用于积分导出，如果传参表示勾选数据导出
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/common/userPointsManage/userPointsExport"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "nickName": nickName,  # 用户昵称
        "mobile": mobile,  # 用户手机号
        "beginTime": beginTime,  # 注册时间查询范围--开始时间
        "endTime": endTime,  # 注册时间查询范围--结束时间
        "logIds": logIds,  # 积分明细Id，用于积分导出，如果传参表示勾选数据导出
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/common/userPointsManage/page")
def common_userpointsmanage_page(nickName=None, mobile=None, endTime=None, beginTime=None, headers=None, **kwargs):
    """
    用户积分列表查询-历史接口
    up_time=1676338867

    params: nickName :  : 
    params: mobile :  : 
    params: beginTime :  : 前端日期后面必须要追加 00:00:00
    params: endTime :  : 前端日期后面必须要追加 23:59:59
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : object : 
              records : array : 
              total : number : 总数量
              size : number : 页码大小
              current : number : 当前页码
              pages : number : 总页码数
    """
    _method = "GET"
    _url = "/common/userPointsManage/page"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "nickName": nickName,
        "mobile": mobile,
        "beginTime": beginTime,  # 前端日期后面必须要追加 00:00:00
        "endTime": endTime,  # 前端日期后面必须要追加 23:59:59
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/common/userPointsManage/manualChangeUserPoints")
def common_userpointsmanage_manualchangeuserpoints(userId=None, operateMark=None, operatePoint=None, pointChangType=None, taskName=None, operateType=None, headers=None, **kwargs):
    """
    用户积分手动调整-历史接口
    up_time=1676338835

    params: userId : number : 用户id
    params: operateType : string : 积分操作类型 目前只有 “增加” 一类
    params: operatePoint : integer : 操作的积分数量
    params: operateMark : string : 操作的积分备注
    params: taskName : string : 任务名称 注册 签到 消费
    params: pointChangType : number : 1--增加  2--消耗
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/common/userPointsManage/manualChangeUserPoints"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户id
        "operateType": operateType,  # 积分操作类型 目前只有 “增加” 一类
        "operatePoint": operatePoint,  # 操作的积分数量
        "operateMark": operateMark,  # 操作的积分备注
        "taskName": taskName,  # 任务名称 注册 签到 消费
        "pointChangType": pointChangType,  # 1--增加  2--消耗
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/common/userPointsManage/beforePointsExport")
def common_userpointsmanage_beforepointsexport(nickName=None, beginTime=None, mobile=None, logIds=None, endTime=None, headers=None, **kwargs):
    """
    积分导出前置判断-历史接口
    up_time=1676338890

    params: nickName :  : 用户昵称
    params: mobile :  : 用户手机号
    params: beginTime :  : 注册时间查询范围--开始时间
    params: endTime :  : 注册时间查询范围--结束时间
    params: logIds :  : 积分明细Id，用于积分导出，如果传参表示勾选数据导出
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功
    params: msg : string : 描述
    params: data : boolean : true 调用积分导出方法
    """
    _method = "GET"
    _url = "/common/userPointsManage/beforePointsExport"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "nickName": nickName,  # 用户昵称
        "mobile": mobile,  # 用户手机号
        "beginTime": beginTime,  # 注册时间查询范围--开始时间
        "endTime": endTime,  # 注册时间查询范围--结束时间
        "logIds": logIds,  # 积分明细Id，用于积分导出，如果传参表示勾选数据导出
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


