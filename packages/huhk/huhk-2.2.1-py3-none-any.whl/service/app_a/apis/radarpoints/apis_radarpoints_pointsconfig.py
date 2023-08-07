import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/radarpoints/PointsConfig/page")
def radarpoints_pointsconfig_page(pointsBegin=None, Current=None, status=None, name=None, pointsEnd=None, pointsExpiration=None, size=None, code=None, businessSceneType=None, headers=None, **kwargs):
    """
    积分配置 - 分页查询
    up_time=1680142594

    params: code :  : 积分项Code
    params: name :  : 积分项名称
    params: businessSceneType :  : 发放场景类型
    params: pointsBegin :  : 积分值 - 开始区间
    params: pointsEnd :  : 积分值 - 结束区间
    params: pointsExpiration :  : 积分有效期
    params: status :  : 生效状态（0未生效，1已生效）
    params: Current :  : 当前页
    params: size :  : 每页大小
    params: headers : 请求头
    ====================返回======================
    params: code : integer : 
    params: msg : string : 
    params: data : object : 
              code : string : 积分项编码
              name : string : 积分项名称
              businessSceneType : string : 发放场景类型
              points : integer : 积分值
              toast : string : toast内容
              PointsExpiration : string : 积分有效期
              status : integer : 状态值
              statusName : string : 状态名称
              remark : string : 备注
              rulesPointsDayMax : integer : 积分获取-分数上限
              userPointsDayMax : integer : 单用户单日上限
              pointsOperator : string : bpm单号
              bpmId : string : 积分操作者
    """
    _method = "GET"
    _url = "/radarpoints/PointsConfig/page"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "code": code,  # 积分项Code
        "name": name,  # 积分项名称
        "businessSceneType": businessSceneType,  # 发放场景类型
        "pointsBegin": pointsBegin,  # 积分值 - 开始区间
        "pointsEnd": pointsEnd,  # 积分值 - 结束区间
        "pointsExpiration": pointsExpiration,  # 积分有效期
        "status": status,  # 生效状态（0未生效，1已生效）
        "Current": Current,  # 当前页
        "size": size,  # 每页大小
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/radarpoints/PointsConfig/insert")
def radarpoints_pointsconfig_insert(remark=None, rulesPointsDayMax=None, businessSceneType=None, pointsExpiration=None, userPointsDayMax=None, toast=None, bpmId=None, points=None, name=None, headers=None, **kwargs):
    """
    积分配置 -新增积分配置
    up_time=1680142659

    params: pointsExpiration : string : 积分有效期
    params: remark : string : 备注
    params: points : integer : 积分值
    params: toast : string : toast内容
    params: name : string : 积分项名称
    params: businessSceneType : integer : 发放场景类型
    params: bpmId : integer : bpm单号
    params: userPointsDayMax : integer : 单用户单日上限
    params: rulesPointsDayMax : integer : 单日上限
    params: headers : 请求头
    ====================返回======================
    params: code : integer : 
    params: msg : string : 
    params: data : string : 
    """
    _method = "POST"
    _url = "/radarpoints/PointsConfig/insert"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "pointsExpiration": pointsExpiration,  # 积分有效期
        "remark": remark,  # 备注
        "points": points,  # 积分值
        "toast": toast,  # toast内容
        "name": name,  # 积分项名称
        "businessSceneType": businessSceneType,  # 发放场景类型
        "bpmId": bpmId,  # bpm单号
        "userPointsDayMax": userPointsDayMax,  # 单用户单日上限
        "rulesPointsDayMax": rulesPointsDayMax,  # 单日上限
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/radarpoints/PointsConfig/update")
def radarpoints_pointsconfig_update(remark=None, id=None, rulesPointsDayMax=None, businessSceneType=None, pointsExpiration=None, code=None, userPointsDayMax=None, toast=None, bpmId=None, points=None, name=None, headers=None, **kwargs):
    """
    积分配置 -修改积分配置
    up_time=1680142897

    params: pointsExpiration : string : 积分有效期
    params: remark : string : 备注
    params: points : integer : 积分值
    params: toast : string : toast内容
    params: name : string : 积分项名称
    params: businessSceneType : integer : 发放场景类型
    params: id : integer : 积分项id
    params: code : string : 积分项code
    params: rulesPointsDayMax : integer : 单日上限
    params: userPointsDayMax : integer : 单用户单日上限
    params: bpmId : integer : bpm单号
    params: headers : 请求头
    ====================返回======================
    params: code : integer : 
    params: msg : string : 
    params: data : string : 
    """
    _method = "POST"
    _url = "/radarpoints/PointsConfig/update"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "pointsExpiration": pointsExpiration,  # 积分有效期
        "remark": remark,  # 备注
        "points": points,  # 积分值
        "toast": toast,  # toast内容
        "name": name,  # 积分项名称
        "businessSceneType": businessSceneType,  # 发放场景类型
        "id": id,  # 积分项id
        "code": code,  # 积分项code
        "rulesPointsDayMax": rulesPointsDayMax,  # 单日上限
        "userPointsDayMax": userPointsDayMax,  # 单用户单日上限
        "bpmId": bpmId,  # bpm单号
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/radarpoints/PointsConfig/updateStatusById")
def radarpoints_pointsconfig_updatestatusbyid(id=None, status=None, headers=None, **kwargs):
    """
    积分配置 -生效状态变更
    up_time=1676455564

    params: id :  : 积分id
    params: status :  : 生效状态（0未生效，1已生效）
    params: headers : 请求头
    ====================返回======================
    params: code : integer : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "GET"
    _url = "/radarpoints/PointsConfig/updateStatusById"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "id": id,  # 积分id
        "status": status,  # 生效状态（0未生效，1已生效）
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


