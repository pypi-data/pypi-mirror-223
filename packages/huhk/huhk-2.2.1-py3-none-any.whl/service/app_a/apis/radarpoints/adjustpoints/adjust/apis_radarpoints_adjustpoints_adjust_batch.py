import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/radarpoints/adjustPoints/adjust/batch/save")
def radarpoints_adjustpoints_adjust_batch_save(redisKey=None, clientNotes=None, optAbilityName=None, adjustNotes=None, file=None, optAbility=None, headers=None, **kwargs):
    """
    积分调整 - 批量调整
    up_time=1677216489

    params: file : file : 导入excel文件
    params: optAbility : text : 调整方式
    params: adjustNotes : text : 调整原因说明
    params: clientNotes : text : 用户端展示
    params: optAbilityName : string : 调整方式枚举
    params: redisKey : string : 缓存键
    params: headers : 请求头
    ====================返回======================
    params: code : number : 200成功，其他-失败
    params: msg : string : 提示信息
    params: data : object : 
              checkErrorNum : number : 此接口不使用
              checkSuccessNum : number : 此接口不使用
              executeErrorNum : number : 执行 - 错误数据
              executeSuccessNum : number : 执行 - 成功数据
              list : array : 
    """
    _method = "POST"
    _url = "/radarpoints/adjustPoints/adjust/batch/save"

    _headers = {
        "Content-Type": "multipart/form-data",
    }
    _headers.update({"headers": headers})

    _data = {
        "file": file,  # 导入excel文件
        "optAbility": optAbility,  # 调整方式
        "adjustNotes": adjustNotes,  # 调整原因说明
        "clientNotes": clientNotes,  # 用户端展示
        "optAbilityName": optAbilityName,  # 调整方式枚举
        "redisKey": redisKey,  # 缓存键
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/radarpoints/adjustPoints/adjust/batch/import")
def radarpoints_adjustpoints_adjust_batch_import(list=None, field_34=None, clientNotes=None, adjustNotes=None, field_35=None, file=None, headers=None, **kwargs):
    """
    积分调整 - 批量调整 - 导入excel
    up_time=1677216494

    params: file : file : excel文件
    params: adjustNotes : string : 调整原因说明
    params: clientNotes : string : 客户端显示信息
    params: list : array : 成功数据集
              userId : number : 用户id
              adjustTypeName : number : 调整类型名称
              adjustNumber : number : 调整数值
              pointsDepartment : number : 积分归属部门
              DateType : number : 生效时间类型
    params: field_35 : string : 
    params: field_34 : string : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 200：成功，其他失败
    params: msg : string : 提示信息
    params: data : object : 
              checkErrorNum : number : Excel校验 - 错误数据
              checkSuccessNum : number : Excel校验 - 成功数据
              executeErrorNum : number : 此接口不使用
              executeSuccessNum : number : 此接口不使用
              list : array : 
    """
    _method = "POST"
    _url = "/radarpoints/adjustPoints/adjust/batch/import"

    _headers = {
        "Content-Type": "multipart/form-data",
    }
    _headers.update({"headers": headers})

    _data = {
        "file": file,  # excel文件
        "adjustNotes": adjustNotes,  # 调整原因说明
        "clientNotes": clientNotes,  # 客户端显示信息
        "list": list,  # 成功数据集
        "field_35": field_35,
        "field_34": field_34,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


