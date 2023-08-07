import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/radarpoints/summaryStatistics/pageList")
def radarpoints_summarystatistics_pagelist(current=None, flowTimeBefore=None, size=None, flowTimeEnd=None, headers=None, **kwargs):
    """
    积分汇总统计-分页查询积分
    up_time=1676623470

    params: current :  : 
    params: size :  : 
    params: flowTimeBefore :  : 流水开始时间
    params: flowTimeEnd :  : 流水结束时间
    params: headers : 请求头
    ====================返回======================
    params: code : string : 
    params: msg : string : 
    params: data : object : 
              records : array : 
              size : string : 
              current : string : 
              total : string : 
    """
    _method = "GET"
    _url = "/radarpoints/summaryStatistics/pageList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,
        "size": size,
        "flowTimeBefore": flowTimeBefore,  # 流水开始时间
        "flowTimeEnd": flowTimeEnd,  # 流水结束时间
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/radarpoints/summaryStatistics/export")
def radarpoints_summarystatistics_export(current=None, flowTimebefore=None, size=None, flowTimeEnd=None, headers=None, **kwargs):
    """
    积分汇总统计 - 导出
    up_time=1676625526

    params: current :  : 
    params: size :  : 
    params: flowTimeEnd :  : 
    params: flowTimebefore :  : 
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/radarpoints/summaryStatistics/export"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,
        "size": size,
        "flowTimeEnd": flowTimeEnd,
        "flowTimebefore": flowTimebefore,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


