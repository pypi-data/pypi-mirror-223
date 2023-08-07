import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/radarpoints/adjustPoints/adjust/single/save")
def radarpoints_adjustpoints_adjust_single_save(userId=None, clientNotes=None, qty=None, pointsExpiration=None, adjustNotes=None, optAbility=None, headers=None, **kwargs):
    """
    积分调整 - 单次调整
    up_time=1677216484

    params: optAbility : number : 积分调整类型
    params: adjustNotes : string : 调整原因说明
    params: clientNotes : string : 户端展示信息
    params: userId : number : 调整目标用户ID
    params: qty : number : 调整数值
    params: pointsExpiration : number : 积分有效期类型（新增时赋值）
    params: headers : 请求头
    ====================返回======================
    params: code : number : 200：成功，其他失败
    params: msg : string : 备注
    params: data : boolean : true/false
    """
    _method = "POST"
    _url = "/radarpoints/adjustPoints/adjust/single/save"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "optAbility": optAbility,  # 积分调整类型
        "adjustNotes": adjustNotes,  # 调整原因说明
        "clientNotes": clientNotes,  # 户端展示信息
        "userId": userId,  # 调整目标用户ID
        "qty": qty,  # 调整数值
        "pointsExpiration": pointsExpiration,  # 积分有效期类型（新增时赋值）
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


