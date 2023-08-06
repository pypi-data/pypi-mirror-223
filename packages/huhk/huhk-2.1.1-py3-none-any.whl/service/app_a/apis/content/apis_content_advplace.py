import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/advplace/updateName")
def content_advplace_updatename(advPlaceName=None, advPlaceId=None, playTime=None, startFlag=None, headers=None, **kwargs):
    """
    点位-更新大点位内容
    up_time=1675133826

    params: advPlaceId : text : 
    params: advPlaceName : text : 
    params: startFlag : text : 广告页广告位必传
    params: playTime : text : 广告页广告位必传
    params: headers : 请求头
    ====================返回======================
    """
    _method = "POST"
    _url = "/content/advplace/updateName"

    _headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    _headers.update({"headers": headers})

    _data = {
        "advPlaceId": advPlaceId,
        "advPlaceName": advPlaceName,
        "startFlag": startFlag,  # 广告页广告位必传
        "playTime": playTime,  # 广告页广告位必传
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


