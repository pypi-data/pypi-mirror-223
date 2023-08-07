import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/radarpoints/pointsTask/pageList")
def radarpoints_pointstask_pagelist(pointsTaskDateSort=None, dateLast=None, pointsConfigCode=None, pointsConfigName=None, current=None, mobile=None, getPointsQtySort=None, dateBegin=None, size=None, headers=None, **kwargs):
    """
    积分任务 - 分页查询
    up_time=1679971837

    params: dateBegin :  : 开始日期
    params: dateLast :  : 结束日期
    params: pointsConfigCode :  : 任务编码
    params: pointsConfigName :  : 任务名称
    params: mobile :  : 用户手机号
    params: pointsTaskDateSort :  : 日期排序字段，"ASC"升序，"DESC"降序
    params: getPointsQtySort :  : 积分值排序字段，"ASC"升序，"DESC"降序
    params: current :  : 页码
    params: size :  : 每页大小
    params: headers : 请求头
    ====================返回======================
    params: code : number : 200：成功
    params: msg : string : 信息
    params: data : object : 数据
              records : array : 分页数据
              total : string : 总条数
              current : string : 页码
              size : string : 每页大小
              pages : number : 总页数
    """
    _method = "GET"
    _url = "/radarpoints/pointsTask/pageList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "dateBegin": dateBegin,  # 开始日期
        "dateLast": dateLast,  # 结束日期
        "pointsConfigCode": pointsConfigCode,  # 任务编码
        "pointsConfigName": pointsConfigName,  # 任务名称
        "mobile": mobile,  # 用户手机号
        "pointsTaskDateSort": pointsTaskDateSort,  # 日期排序字段，"ASC"升序，"DESC"降序
        "getPointsQtySort": getPointsQtySort,  # 积分值排序字段，"ASC"升序，"DESC"降序
        "current": current,  # 页码
        "size": size,  # 每页大小
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/radarpoints/pointsTask/export")
def radarpoints_pointstask_export(pointsTaskDateSort=None, dateLast=None, pointsConfigCode=None, pointsConfigName=None, mobile=None, getPointsQtySort=None, dateBegin=None, headers=None, **kwargs):
    """
    积分任务 - 导出excel
    up_time=1679971864

    params: dateBegin :  : 开始日期
    params: dateLast :  : 结束日期
    params: pointsConfigCode :  : 任务编码
    params: pointsConfigName :  : 任务名称
    params: mobile :  : 用户手机号
    params: pointsTaskDateSort :  : 日期排序字段，"ASC"升序，"DESC"降序
    params: getPointsQtySort :  : 积分值排序字段，"ASC"升序，"DESC"降序
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/radarpoints/pointsTask/export"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "dateBegin": dateBegin,  # 开始日期
        "dateLast": dateLast,  # 结束日期
        "pointsConfigCode": pointsConfigCode,  # 任务编码
        "pointsConfigName": pointsConfigName,  # 任务名称
        "mobile": mobile,  # 用户手机号
        "pointsTaskDateSort": pointsTaskDateSort,  # 日期排序字段，"ASC"升序，"DESC"降序
        "getPointsQtySort": getPointsQtySort,  # 积分值排序字段，"ASC"升序，"DESC"降序
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


