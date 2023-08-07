import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/radarpoints/userPoints/pageList")
def radarpoints_userpoints_pagelist(cumulativeAcquisitionMost=None, userId=None, registrationTimeBegin=None, physicalIntegralLeast=None, nickName=None, cumulativeAcquisitionLeast=None, freezeQtyLeast=None, current=None, conversionFrequencyLeast=None, registrationTimeEnd=None, mobile=None, physicalIntegralMost=None, cumulativeConsumptionLeast=None, conversionFrequencyMost=None, freezeQtyMost=None, size=None, cumulativeConsumptionMost=None, headers=None, **kwargs):
    """
    用户积分 - 分页查询
    up_time=1677209132

    params: userId :  : 用户id
    params: mobile :  : 用户手机号
    params: nickName :  : 用户昵称
    params: registrationTimeBegin :  : 注册时间 - 开始
    params: registrationTimeEnd :  : 注册时间 - 结束
    params: physicalIntegralLeast :  : 持有积分 - 最少
    params: physicalIntegralMost :  : 持有积分 - 最多
    params: cumulativeAcquisitionLeast :  : 累计获取 - 最少
    params: cumulativeAcquisitionMost :  : 累计获取 - 最多
    params: cumulativeConsumptionLeast :  : 累计消耗 - 最少
    params: cumulativeConsumptionMost :  : 累计消耗 - 最多
    params: conversionFrequencyLeast :  : 兑换次数 - 最少
    params: conversionFrequencyMost :  : 兑换次数 - 最多
    params: freezeQtyLeast :  : 冻结积分 - 最少
    params: freezeQtyMost :  : 冻结积分 - 最多
    params: current :  : 页码
    params: size :  : 每页大小
    params: headers : 请求头
    ====================返回======================
    params: code : number : 200：成功，其他：失败
    params: msg : string : 备注
    params: data : object : 数据
              current : number : 页码
              pages : number : 总页数
              size : number : 每页大小
              total : number : 数据总数
              records : array : list
    """
    _method = "GET"
    _url = "/radarpoints/userPoints/pageList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户id
        "mobile": mobile,  # 用户手机号
        "nickName": nickName,  # 用户昵称
        "registrationTimeBegin": registrationTimeBegin,  # 注册时间 - 开始
        "registrationTimeEnd": registrationTimeEnd,  # 注册时间 - 结束
        "physicalIntegralLeast": physicalIntegralLeast,  # 持有积分 - 最少
        "physicalIntegralMost": physicalIntegralMost,  # 持有积分 - 最多
        "cumulativeAcquisitionLeast": cumulativeAcquisitionLeast,  # 累计获取 - 最少
        "cumulativeAcquisitionMost": cumulativeAcquisitionMost,  # 累计获取 - 最多
        "cumulativeConsumptionLeast": cumulativeConsumptionLeast,  # 累计消耗 - 最少
        "cumulativeConsumptionMost": cumulativeConsumptionMost,  # 累计消耗 - 最多
        "conversionFrequencyLeast": conversionFrequencyLeast,  # 兑换次数 - 最少
        "conversionFrequencyMost": conversionFrequencyMost,  # 兑换次数 - 最多
        "freezeQtyLeast": freezeQtyLeast,  # 冻结积分 - 最少
        "freezeQtyMost": freezeQtyMost,  # 冻结积分 - 最多
        "current": current,  # 页码
        "size": size,  # 每页大小
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/radarpoints/userPoints/export")
def radarpoints_userpoints_export(cumulativeAcquisitionMost=None, registrationTimeBegin=None, physicalIntegralLeast=None, pageSize=None, nickName=None, cumulativeAcquisitionLeast=None, conversionFrequencyLeast=None, registrationTimeEnd=None, currentPage=None, physicalIntegralMost=None, cumulativeConsumptionLeast=None, conversionFrequencyMost=None, cumulativeConsumptionMost=None, headers=None, **kwargs):
    """
    用户积分 - 导出excel
    up_time=1677216441

    params: nickName :  : 用户昵称
    params: registrationTimeBegin :  : 注册时间 - 开始
    params: registrationTimeEnd :  : 注册时间 - 结束
    params: physicalIntegralLeast :  : 持有积分 - 最少
    params: physicalIntegralMost :  : 持有积分 - 最多
    params: cumulativeAcquisitionLeast :  : 累计获取 - 最少
    params: cumulativeAcquisitionMost :  : 累计获取 - 最多
    params: cumulativeConsumptionLeast :  : 累计消耗 - 最少
    params: cumulativeConsumptionMost :  : 累计消耗 - 最多
    params: conversionFrequencyLeast :  : 兑换次数 - 最少
    params: conversionFrequencyMost :  : 兑换次数 - 最多
    params: currentPage :  : 当前页码
    params: pageSize :  : 每页大小
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/radarpoints/userPoints/export"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "nickName": nickName,  # 用户昵称
        "registrationTimeBegin": registrationTimeBegin,  # 注册时间 - 开始
        "registrationTimeEnd": registrationTimeEnd,  # 注册时间 - 结束
        "physicalIntegralLeast": physicalIntegralLeast,  # 持有积分 - 最少
        "physicalIntegralMost": physicalIntegralMost,  # 持有积分 - 最多
        "cumulativeAcquisitionLeast": cumulativeAcquisitionLeast,  # 累计获取 - 最少
        "cumulativeAcquisitionMost": cumulativeAcquisitionMost,  # 累计获取 - 最多
        "cumulativeConsumptionLeast": cumulativeConsumptionLeast,  # 累计消耗 - 最少
        "cumulativeConsumptionMost": cumulativeConsumptionMost,  # 累计消耗 - 最多
        "conversionFrequencyLeast": conversionFrequencyLeast,  # 兑换次数 - 最少
        "conversionFrequencyMost": conversionFrequencyMost,  # 兑换次数 - 最多
        "currentPage": currentPage,  # 当前页码
        "pageSize": pageSize,  # 每页大小
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


