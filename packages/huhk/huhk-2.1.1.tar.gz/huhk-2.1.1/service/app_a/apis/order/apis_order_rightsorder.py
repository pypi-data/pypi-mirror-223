import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/order/rightsOrder/export")
def order_rightsorder_export(payDateBegin=None, userId=None, orderMainId=None, payDateEnd=None, receiveDateBegin=None, receiveDateEnd=None, useStatus=None, rightsType=None, mobile=None, rightsOrderId=None, headers=None, **kwargs):
    """
    权益订单导出接口-Y
    up_time=1675414281

    params: userId :  : 用户ID
    params: mobile :  : 手机号码
    params: rightsOrderId :  : 权益订单ID
    params: orderMainId :  : 主订单ID
    params: useStatus :  : 权益使用状态
    params: rightsType :  : 权益类型
    params: receiveDateBegin :  : 权益领取时间 - 开始
    params: receiveDateEnd :  : 权益领取时间 - 结束
    params: payDateBegin :  : 权益支付时间 - 开始
    params: payDateEnd :  : 权益支付时间 - 结束
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/order/rightsOrder/export"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
        "mobile": mobile,  # 手机号码
        "rightsOrderId": rightsOrderId,  # 权益订单ID
        "orderMainId": orderMainId,  # 主订单ID
        "useStatus": useStatus,  # 权益使用状态
        "rightsType": rightsType,  # 权益类型
        "receiveDateBegin": receiveDateBegin,  # 权益领取时间 - 开始
        "receiveDateEnd": receiveDateEnd,  # 权益领取时间 - 结束
        "payDateBegin": payDateBegin,  # 权益支付时间 - 开始
        "payDateEnd": payDateEnd,  # 权益支付时间 - 结束
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/rightsOrder/insert")
def order_rightsorder_insert(orderMainId=None, userId=None, rightsId=None, createBy=None, payDate=None, createTime=None, refundDate=None, payBillNo=None, useStatus=None, rightsType=None, rightsName=None, payAmount=None, mobile=None, receiveDate=None, refundBillNo=None, updateId=None, updateTime=None, rightsOrderId=None, headers=None, **kwargs):
    """
    权益订单 - 新增-Y
    up_time=1675413078

    params: rightsOrderId : number : 权益订单ID
    params: rightsId : number : 权益ID
    params: rightsType : integer : 权益类型
    params: rightsName : string : 权益名称
    params: orderMainId : string : 主订单ID
    params: userId : number : 用户ID
    params: mobile : string : 用户手机号
    params: payAmount : string : 支付金额
    params: useStatus : integer : 权益使用状态
    params: receiveDate : string : 权益领取时间
    params: payDate : string : 权益支付时间
    params: refundDate : string : 权益退款时间
    params: payBillNo : string : 支付流水
    params: refundBillNo : string : 退款流水
    params: createTime : string : 创建时间
    params: createBy : number : 创建人
    params: updateTime : string : 更新时间
    params: updateId : number : 更新人id
    params: headers : 请求头
    ====================返回======================
    params: code : string : 
    params: msg : string : 
    params: data : string : 
    """
    _method = "POST"
    _url = "/order/rightsOrder/insert"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "rightsOrderId": rightsOrderId,  # 权益订单ID
        "rightsId": rightsId,  # 权益ID
        "rightsType": rightsType,  # 权益类型
        "rightsName": rightsName,  # 权益名称
        "orderMainId": orderMainId,  # 主订单ID
        "userId": userId,  # 用户ID
        "mobile": mobile,  # 用户手机号
        "payAmount": payAmount,  # 支付金额
        "useStatus": useStatus,  # 权益使用状态
        "receiveDate": receiveDate,  # 权益领取时间
        "payDate": payDate,  # 权益支付时间
        "refundDate": refundDate,  # 权益退款时间
        "payBillNo": payBillNo,  # 支付流水
        "refundBillNo": refundBillNo,  # 退款流水
        "createTime": createTime,  # 创建时间
        "createBy": createBy,  # 创建人
        "updateTime": updateTime,  # 更新时间
        "updateId": updateId,  # 更新人id
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/rightsOrder/page")
def order_rightsorder_page(payDateBegin=None, userId=None, orderMainId=None, payDateEnd=None, receiveDateBegin=None, current=None, receiveDateEnd=None, useStatus=None, rightsType=None, mobile=None, rightsOrderId=None, size=None, headers=None, **kwargs):
    """
    权益订单 - 分页查询-Y
    up_time=1675412172

    params: size :  : 
    params: current :  : 
    params: userId :  : 用户ID
    params: mobile :  : 手机号码 
    params: rightsOrderId :  : 权益订单ID
    params: orderMainId :  : 主订单ID
    params: useStatus :  : 权益使用状态
    params: rightsType :  : 权益类型
    params: receiveDateBegin :  : 权益领取时间 开始
    params: receiveDateEnd :  : 权益领取时间-结束
    params: payDateBegin :  : 权益支付时间 - 开始
    params: payDateEnd :  : 权益支付时间 - 结束
    params: headers : 请求头
    ====================返回======================
    params: code : string : 
    params: msg : string : 
    params: data : object : 
              records : array : 
              total : number : 
              size : number : 
              current : number : 
    """
    _method = "GET"
    _url = "/order/rightsOrder/page"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "size": size,
        "current": current,
        "userId": userId,  # 用户ID
        "mobile": mobile,  # 手机号码 
        "rightsOrderId": rightsOrderId,  # 权益订单ID
        "orderMainId": orderMainId,  # 主订单ID
        "useStatus": useStatus,  # 权益使用状态
        "rightsType": rightsType,  # 权益类型
        "receiveDateBegin": receiveDateBegin,  # 权益领取时间 开始
        "receiveDateEnd": receiveDateEnd,  # 权益领取时间-结束
        "payDateBegin": payDateBegin,  # 权益支付时间 - 开始
        "payDateEnd": payDateEnd,  # 权益支付时间 - 结束
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/rightsOrder/receive")
def order_rightsorder_receive(orderId=None, rightsId=None, headers=None, **kwargs):
    """
    权益-领取权益-Y
    up_time=1675660702

    params: orderId : string : 子订单ID
    params: rightsId : number : 权益ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              orderMainId : string : 主订单ID
              userId : number : 用户ID
              mobile : string : 用户手机号
              rightsOrderId : number : 权益订单ID
              rightsId : string : 权益ID
              rightsType : integer : 权益类型
              rightsName : string : 权益名称
              payAmount : string : 支付金额
              useStatus : string : 权益使用状态
              receiveDate : string : 权益领取时间
              createTime : string : 创建时间
              createBy : number : 创建人
              delFlag : integer : 删除标识 0：否 1：是
              field_160 : string : 用户手机号
    """
    _method = "POST"
    _url = "/order/rightsOrder/receive"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "orderId": orderId,  # 子订单ID
        "rightsId": rightsId,  # 权益ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/rightsOrder/getOrderList")
def order_rightsorder_getorderlist(useStatusList=None, orderMainId=None, rightsType=None, rightsNameList=None, mobile=None, receiveDate=None, headers=None, **kwargs):
    """
    权益订单 - 查询-Y
    up_time=1675413979

    params: orderMainId : number : 主订单ID
    params: rightsType : integer : 权益类型
    params: rightsNameList : array : 权益名称
              type : string : None
    params: useStatusList : array : 权益使用状态
              type : integer : None
    params: mobile : string : 用户手机号
    params: receiveDate : string : 权益领取时间
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : array : 
              rightsOrderId : number : 权益订单ID
              rightsId : number : 权益ID
              rightsType : integer : 权益类型
              rightsName : string : 权益名称
              rightsInfo : object : 权益信息
              orderMainId : string : 主订单ID
              userId : string : 用户ID
              mobile : string : 用户手机号
              payAmount : string : 支付金额
              useStatus : integer : 权益使用状态 (10未使用、20使用中、30使用成功、40使用失败、50已失效)
              useStatusName : string : 权益使用状态名称
              receiveDate : string : 权益领取时间
              payDate : string : 权益支付时间
              refundDate : string : 权益退款时间
              payBillNo : string : 支付流水
              refundBillNo : string : 退款流水
              createTime : string : 创建时间
              createBy : number : 创建人
              updateTime : string : 更新时间
              updateId : number : 更新人id
    """
    _method = "POST"
    _url = "/order/rightsOrder/getOrderList"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "orderMainId": orderMainId,  # 主订单ID
        "rightsType": rightsType,  # 权益类型
        "rightsNameList": rightsNameList,  # 权益名称
        "useStatusList": useStatusList,  # 权益使用状态
        "mobile": mobile,  # 用户手机号
        "receiveDate": receiveDate,  # 权益领取时间
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/rightsOrder/statusUpdate")
def order_rightsorder_statusupdate(workStatus=None, soNo=None, headers=None, **kwargs):
    """
    更新充电桩订单状态-Y
    up_time=1675414502

    params: soNo :  : 第三方订单
    params: workStatus :  : 权益使用状态
    params: headers : 请求头
    ====================返回======================
    params: code : integer : 0失败1成功
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "GET"
    _url = "/order/rightsOrder/statusUpdate"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "soNo": soNo,  # 第三方订单
        "workStatus": workStatus,  # 权益使用状态
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


