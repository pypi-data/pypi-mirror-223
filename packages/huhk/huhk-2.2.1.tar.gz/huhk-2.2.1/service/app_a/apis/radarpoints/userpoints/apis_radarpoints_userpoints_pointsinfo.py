import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/radarpoints/userPoints/pointsInfo/pageList")
def radarpoints_userpoints_pointsinfo_pagelist(userId=None, current=None, changeTimeBegin=None, changeTimeEnd=None, name=None, size=None, businessSceneType=None, headers=None, **kwargs):
    """
    用户中心-积分明细-分页查询
    up_time=1677054547

    params: userId :  : 用户ID
    params: size :  : 每页大小
    params: current :  : 当前页
    params: businessSceneType :  : 10001 转介裂变
10002 营销活动
10003 社区活跃
10004 线下活动
10005 用车行为
10006 评价
10007 内容奖励
10008 后台管理手动操作
20000 其他
    params: name :  : 名称
    params: changeTimeBegin :  : 变动开始时间
    params: changeTimeEnd :  : 变动结束时间
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              records : array : 
              size : number : 每页大小
              current : number : 当前页
              total : number : 总页数
    """
    _method = "GET"
    _url = "/radarpoints/userPoints/pointsInfo/pageList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
        "size": size,  # 每页大小
        "current": current,  # 当前页
        "businessSceneType": businessSceneType,  # 10001 转介裂变 10002 营销活动 10003 社区活跃 10004 线下活动 10005 用车行为 10006 评价 10007 内容奖励 10008 后台管理手动操作 20000 其他
        "name": name,  # 名称
        "changeTimeBegin": changeTimeBegin,  # 变动开始时间
        "changeTimeEnd": changeTimeEnd,  # 变动结束时间
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


