import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/activityManager/updateActivityTop")
def activitymanager_updateactivitytop(activityId=None, topFlag=None, headers=None, **kwargs):
    """
    后台管理-置顶接口-Y
    up_time=1675649321

    params: activityId : string : 活动主键
    params: topFlag : integer : 活动置顶标识 0-不置顶 1-置顶
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/activityManager/updateActivityTop"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "activityId": activityId,  # 活动主键
        "topFlag": topFlag,  # 活动置顶标识 0-不置顶 1-置顶
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


