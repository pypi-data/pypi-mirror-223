import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/radarpoints/adjustPoints/pageList")
def radarpoints_adjustpoints_pagelist(userId=None, nickName=None, current=None, optAbilityName=None, adjustTimeEnd=None, mobile=None, size=None, adjustNotes=None, optAbility=None, adjustTimeBefore=None, headers=None, **kwargs):
    """
    积分调整 - 分页查询
    up_time=1677209059

    params: userId :  : 用户id
    params: nickName :  : 用户名
    params: mobile :  : 手机号
    params: adjustNotes :  : 调整原因说明
    params: optAbility :  : 调整积分方式
    params: optAbilityName :  : 调整积分方式枚举
    params: adjustTimeBefore :  : 调整时间 - 开始
    params: adjustTimeEnd :  : 调整时间 - 结束
    params: current :  : 页码
    params: size :  : 每页大小
    params: headers : 请求头
    ====================返回======================
    params: code : number : 200：成功，其他失败
    params: msg : string : 信息
    params: data : array : 分页数据
              current : number : 页码
              pages : number : 总页数
              size : number : 每页大小
              total : number : 数据总数
              records : array : list
    """
    _method = "GET"
    _url = "/radarpoints/adjustPoints/pageList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户id
        "nickName": nickName,  # 用户名
        "mobile": mobile,  # 手机号
        "adjustNotes": adjustNotes,  # 调整原因说明
        "optAbility": optAbility,  # 调整积分方式
        "optAbilityName": optAbilityName,  # 调整积分方式枚举
        "adjustTimeBefore": adjustTimeBefore,  # 调整时间 - 开始
        "adjustTimeEnd": adjustTimeEnd,  # 调整时间 - 结束
        "current": current,  # 页码
        "size": size,  # 每页大小
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/radarpoints/adjustPoints/getUserPointsQtyByUserId")
def radarpoints_adjustpoints_getuserpointsqtybyuserid(userId=None, headers=None, **kwargs):
    """
    积分调整 - 根据UserId查询详情
    up_time=1677458192

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 200-成功，其他-失败
    params: msg : string : 提示信息
    params: data : object : 
              userId : string : 用户ID
              mobile : string : 手机号码
              nickName : string : 昵称
              avatarUrl : string : 头像
              physicalQty : integer : 可用积分
              freezeQty : integer : 冻结积分
    """
    _method = "GET"
    _url = "/radarpoints/adjustPoints/getUserPointsQtyByUserId"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/radarpoints/adjustPoints/getUserPointsQtyByMobile")
def radarpoints_adjustpoints_getuserpointsqtybymobile(mobile=None, headers=None, **kwargs):
    """
    积分调整 - 根据Mobile查询详情
    up_time=1677206085

    params: mobile :  : 手机号码
    params: headers : 请求头
    ====================返回======================
    params: code : number : 200-成功，其他-失败
    params: msg : string : 提示信息
    params: data : object : 
              userId : string : 用户ID
              mobile : string : 手机号码
              nickName : string : 昵称
              avatarUrl : string : 头像地址
              physicalQty : integer : 可用积分
              freezeQty : integer : 冻结积分
    """
    _method = "GET"
    _url = "/radarpoints/adjustPoints/getUserPointsQtyByMobile"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "mobile": mobile,  # 手机号码
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/radarpoints/adjustPoints/export")
def radarpoints_adjustpoints_export(userId=None, nickName=None, current=None, optAbilityName=None, adjustTimeEnd=None, mobile=None, size=None, adjustNotes=None, optAbility=None, adjustTimeBefore=None, headers=None, **kwargs):
    """
    积分调整 - 导出excel
    up_time=1677216479

    params: userId :  : 用户id
    params: nickName :  : 用户名
    params: mobile :  : 手机号
    params: adjustNotes :  : 调整原因说明
    params: optAbility :  : 调整积分方式
    params: optAbilityName :  : 调整积分方式枚举
    params: adjustTimeBefore :  : 调整时间 - 开始
    params: adjustTimeEnd :  : 调整时间 - 结束
    params: current :  : 页码
    params: size :  : 每页大小
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/radarpoints/adjustPoints/export"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户id
        "nickName": nickName,  # 用户名
        "mobile": mobile,  # 手机号
        "adjustNotes": adjustNotes,  # 调整原因说明
        "optAbility": optAbility,  # 调整积分方式
        "optAbilityName": optAbilityName,  # 调整积分方式枚举
        "adjustTimeBefore": adjustTimeBefore,  # 调整时间 - 开始
        "adjustTimeEnd": adjustTimeEnd,  # 调整时间 - 结束
        "current": current,  # 页码
        "size": size,  # 每页大小
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


