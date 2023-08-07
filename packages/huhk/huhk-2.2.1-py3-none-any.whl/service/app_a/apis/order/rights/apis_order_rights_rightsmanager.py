import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/order/rights/rightsManager/createId")
def order_rights_rightsmanager_createid( headers=None, **kwargs):
    """
    自动生成权益ID-Y
    up_time=1675407827

    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : string : 
    """
    _method = "GET"
    _url = "/order/rights/rightsManager/createId"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/rights/rightsManager/getRelation")
def order_rights_rightsmanager_getrelation(rightsId=None, headers=None, **kwargs):
    """
    查询互斥关系接口-Y
    up_time=1675409057

    params: rightsId :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0失败1成功
    params: msg : string : 
    params: data : array : 
              rightsId : number : 主键
              rightsName : string : 互斥关系
    """
    _method = "GET"
    _url = "/order/rights/rightsManager/getRelation"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "rightsId": rightsId,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/rights/rightsManager/page")
def order_rights_rightsmanager_page(modelCode=None, current=None, effectiveEndDate=None, status=None, rightsName=None, size=None, headers=None, **kwargs):
    """
    权益 - 分页查询-Y
    up_time=1675409025

    params: size :  : 
    params: current :  : 
    params: rightsName :  : 
    params: status :  : 
    params: modelCode :  : 
    params: effectiveEndDate :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0失败1成
    params: msg : string : 
    params: data : object : 
              records : array : 
              total : number : 
              size : string : 
              current : string : 
    """
    _method = "GET"
    _url = "/order/rights/rightsManager/page"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "size": size,
        "current": current,
        "rightsName": rightsName,
        "status": status,
        "modelCode": modelCode,
        "effectiveEndDate": effectiveEndDate,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/rights/rightsManager/getRightsList")
def order_rights_rightsmanager_getrightslist(modelId=None, effectiveStartDate=None, status=None, rightsName=None, headers=None, **kwargs):
    """
    权益订单 - 查询-Y
    up_time=1675669230

    params: rightsName : string : 权益名称
    params: status : integer : 权益状态(0未生效，1已生效)
    params: modelId : string : 车型代码
    params: effectiveStartDate : string : 权益生效时间
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : array : 
              rightsId : number : 主键
              rightsType : string : 权益类型
              rightsName : string : 权益名称
              content : string : 权益描述
              buyAmount : string : 权益购买金额
              discountAmount : string : 权益优惠金额
              modelId : string : 车型id
              modelCode : string : 车型代码
              orderType : string : 关联订单类型
              relation : string : 互斥关系
              status : integer : 权益状态(0未生效，1已生效)
              effectiveDate : string : 权益生效时间
              effectiveStartDate : string : 权益生效时间 -- 开始
              effectiveEndDate : string : 权益生效时间 -- 结束
              createTime : string : 创建时间
              createBy : number : 创建人
              updateTime : string : 更新时间
              updateId : number : 更新人id
              delFlag : integer : 删除标识 0：否 1：是
              CarModelInfo : object : 
    """
    _method = "POST"
    _url = "/order/rights/rightsManager/getRightsList"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "rightsName": rightsName,  # 权益名称
        "status": status,  # 权益状态(0未生效，1已生效)
        "modelId": modelId,  # 车型代码
        "effectiveStartDate": effectiveStartDate,  # 权益生效时间
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/rights/rightsManager/insert")
def order_rights_rightsmanager_insert(modelCode=None, effectiveStartDate=None, rightsId=None, orderType=None, rightsType=None, rightsName=None, headers=None, **kwargs):
    """
    权益-新增权益-Y
    up_time=1675669334

    params: effectiveStartDate : text : 权益生效时间 -- 开始
    params: rightsId : text : 权益ID
    params: rightsName : text : 权益名称
    params: rightsType : text : 权益类型
    params: modelCode : text : 车型代码
    params: orderType : text : 关联订单类型code
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0失败 1成功
    params: msg : string : 
    params: data : string : 
    """
    _method = "POST"
    _url = "/order/rights/rightsManager/insert"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "effectiveStartDate": effectiveStartDate,  # 权益生效时间 -- 开始
        "rightsId": rightsId,  # 权益ID
        "rightsName": rightsName,  # 权益名称
        "rightsType": rightsType,  # 权益类型
        "modelCode": modelCode,  # 车型代码
        "orderType": orderType,  # 关联订单类型code
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/rights/rightsManager/update")
def order_rights_rightsmanager_update(effectiveStartDate=None, Content=None, rightsId=None, effectiveEndDate=None, rightsName=None, Relation=None, headers=None, **kwargs):
    """
    权益-修改权益-Y
    up_time=1675669374

    params: rightsName : string : 权益名称
    params: rightsId : string : 权益主键
    params: Content : string : 权益描述
    params: effectiveStartDate : string : 权益生效时间
    params: effectiveEndDate : string : 权益生效时间-结束
    params: Relation : string : 互斥关系
    params: headers : 请求头
    ====================返回======================
    params: code : integer : 0失败1成功
    params: msg : string : 
    params: data : string : 
    """
    _method = "POST"
    _url = "/order/rights/rightsManager/update"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "rightsName": rightsName,  # 权益名称
        "rightsId": rightsId,  # 权益主键
        "Content": Content,  # 权益描述
        "effectiveStartDate": effectiveStartDate,  # 权益生效时间
        "effectiveEndDate": effectiveEndDate,  # 权益生效时间-结束
        "Relation": Relation,  # 互斥关系
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/rights/rightsManager/rightsById")
def order_rights_rightsmanager_rightsbyid(id=None, headers=None, **kwargs):
    """
    权益-获取权益详情-Y
    up_time=1675669384

    params: id :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : integer : 0失败 1成功
    params: msg : string : 
    params: data : object : 
              rightsId : number : 主键
              rightsType : integer : 权益类型
              rightsName : string : 权益名称
              content : string : 权益描述
              buyAmount : string : 权益购买金额
              discountAmount : string : 权益优惠金额
              modelId : string : 车型
              orderType : string : 关联订单类型
              relation : string : 互斥关系
              status : string :  权益状态(0未生效，1已生效)
              effectiveDate : string : 权益生效时间
              createTime : string : 创建时间
              createBy : number : 创建人
              updateTime : string : 更新时间
              updateId : number : 更新人id
              delFlag : integer : 删除标识 0：否 1：是
    """
    _method = "GET"
    _url = "/order/rights/rightsManager/rightsById"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "id": id,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/rights/rightsManager/updateStatusById")
def order_rights_rightsmanager_updatestatusbyid(rightsId=None, status=None, headers=None, **kwargs):
    """
    权益-通过id更新权益生效状态-Y
    up_time=1675669396

    params: rightsId :  : 
    params: status :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : integer : 0失败1成功
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "GET"
    _url = "/order/rights/rightsManager/updateStatusById"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "rightsId": rightsId,
        "status": status,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


