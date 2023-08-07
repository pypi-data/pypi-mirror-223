import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/order/mainOrder/pageList")
def order_mainorder_pagelist(current=None, createEndTime=None, sortItems=None, createStartTime=None, size=None, headers=None, **kwargs):
    """
    小订订单分页查询（后台）-Y
    up_time=1683860159

    params: current : string : 
    params: size : string : 
    params: sortItems : string : 排序字段（只能是【orderMain.orderType】、【orderMain.createTime】、【orderPay.createTime】）
    params: createStartTime : string : 订单创建开始日期
    params: createEndTime : string : 订单创建结束日期
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0.成功 1.失败	
    params: msg : string : 
    params: data : object : 
              total : number : 
              list : array : 订单列表
              pageNum : number : 
              pageSize : number : 
              size : number : 
              startRow : number : 
              endRow : number : 
              pages : number : 
              prePage : number : 
              nextPage : number : 
              isFirstPage : boolean : 
              isLastPage : boolean : 
              hasPreviousPage : boolean : 
              hasNextPage : boolean : 
              navigatePages : number : 
              navigatepageNums : null : 
              navigateFirstPage : number : 
              navigateLastPage : number : 
    """
    _method = "POST"
    _url = "/order/mainOrder/pageList"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,
        "size": size,
        "sortItems": sortItems,  # 排序字段（只能是【orderMain.orderType】、【orderMain.createTime】、【orderPay.createTime】）
        "createStartTime": createStartTime,  # 订单创建开始日期
        "createEndTime": createEndTime,  # 订单创建结束日期
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)



@allure.step(title="调接口：/order/mainOrder/downLoad")
def order_mainorder_download(createEndTime=None, orderTypeToSort=None, createStartTime=None, payTimeToSort=None, createTimeToSort=None, headers=None, **kwargs):
    """
    小订订单列表导出（后台）-Y
    up_time=1675326837

    params: orderTypeToSort : string : 订单类型排序 不排序不赋值 正序：asc 倒序：desc
    params: createTimeToSort : string : 订单创建时间 不排序不赋值 正序：asc 倒序：desc
    params: payTimeToSort : string : 订单创建时间 不排序不赋值 正序：asc 倒序：desc
    params: createStartTime : string : 订单创建开始日期
    params: createEndTime : string : 订单创建结束日期
    params: headers : 请求头
    ====================返回======================
    """
    _method = "POST"
    _url = "/order/mainOrder/downLoad"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "orderTypeToSort": orderTypeToSort,  # 订单类型排序 不排序不赋值 正序：asc 倒序：desc
        "createTimeToSort": createTimeToSort,  # 订单创建时间 不排序不赋值 正序：asc 倒序：desc
        "payTimeToSort": payTimeToSort,  # 订单创建时间 不排序不赋值 正序：asc 倒序：desc
        "createStartTime": createStartTime,  # 订单创建开始日期
        "createEndTime": createEndTime,  # 订单创建结束日期
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/mainOrder/detail")
def order_mainorder_detail(orderId=None, headers=None, **kwargs):
    """
    小订订单查询订单详情（后台）-Y
    up_time=1675328256

    params: orderId :  : 订单号
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0.成功 1.失败		
    params: msg : string : 
    params: data : object : 
              orderTypeToSort : null : 
              createTimeToSort : null : 
              payTimeToSort : null : 
              createStartTime : null : 
              createEndTime : null : 
              userId : null : 
              orderId : string : 订单号
              orderStatus : string : 订单状态
              orderStatusName : string : 订单状态名称
              createTime : string : 订单创建时间
              userName : string : 购买人
              mobile : string : 购买人手机号
              prePrice : string : 定金
              totalPrice : string : 总价
              model : null : 
              battery : null : 
              itemList : null : 
              modelPic : null : 
              interiorPic : null : 
              shopVo : null : 
              areaName : null : 
              provinceId : string : 省编码
              cityId : string : 城市编码
              orderType : string : 订单类型
              orderTypeName : null : 订单类型名称
              modelId : string : 车型ID
              existFreeOrder : string : 用户是否存在零元购：0 不存在 1 存在
              existFreeOrderName : string : 用户是否存在零元购名称
              pageSize : number : 
              pageNum : number : 
              total : number : 
              goodsTotal : number : 
              orderProcess : array : 订单链路
              prePricePosterImageUrl : string : 预订金海报图片地址
              modelName : string : 车型名称
              prePriceContent : string : 预订权益内容
              freePriceContent : string : 零元购权益内容
    """
    _method = "GET"
    _url = "/order/mainOrder/detail"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "orderId": orderId,  # 订单号
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/mainOrder/getUserOrderStatusList")
def order_mainorder_getuserorderstatuslist( headers=None, **kwargs):
    """
    订单管理-查询所有用户订单状态-Y
    up_time=1675320292

    params: headers : 请求头
    ====================返回======================
    params: code : integer : 0.成功 1.失败
    params: msg : string : 
    params: data : array : 
              userOrderStatus : string : 用户展示的订单状态
              userOrderStatusName : string : 用户展示的订单状态名称
              sort : integer : 排序
    """
    _method = "GET"
    _url = "/order/mainOrder/getUserOrderStatusList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/mainOrder/getOrderTypeList")
def order_mainorder_getordertypelist( headers=None, **kwargs):
    """
    订单管理-后台查询所有订单类型-Y
    up_time=1675320267

    params: headers : 请求头
    ====================返回======================
    params: code : integer : 0.成功 1.失败
    params: msg : string : 
    params: data : array : 
              orderType : string : 订单类型
              orderTypeName : string : 订单类型名称
              orderTypeProgramLanguage : string : 订单类型程序语言
    """
    _method = "GET"
    _url = "/order/mainOrder/getOrderTypeList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/mainOrder/getExtOrderStatusList")
def order_mainorder_getextorderstatuslist( headers=None, **kwargs):
    """
    订单管理-后台查询所有销售单订单状态-Y
    up_time=1675320328

    params: headers : 请求头
    ====================返回======================
    params: code : integer : 0.成功 1.失败
    params: msg : string : 
    params: data : array : 
              extOrderStatus : string : 第三方订单状态
              extOrderStatusName : string : 第三方订单状态名称
              userOrderStatus : string : 用户展示的订单状态
              userOrderStatusName : string : 用户展示的订单状态名称
              sort : integer : 排序
              showFlag : integer : 下拉框是否显示标识：0不显示，1显示
    """
    _method = "GET"
    _url = "/order/mainOrder/getExtOrderStatusList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/mainOrder/getOrderStatusList")
def order_mainorder_getorderstatuslist( headers=None, **kwargs):
    """
    订单管理-查询所有订单状态-Y
    up_time=1675319495

    params: headers : 请求头
    ====================返回======================
    params: code : number : 0.成功 1.失败
    params: msg : string : 
    params: data : array : 
              orderStatus : string : 订单状态
              orderStatusName : string : 订单状态名称
    """
    _method = "GET"
    _url = "/order/mainOrder/getOrderStatusList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/mainOrder/vinCode")
def order_mainorder_vincode(vin=None, headers=None, **kwargs):
    """
    订单管理-通过vin码查询订单-Y
    up_time=1676969860

    params: vin :  : 车辆唯一vin码
    params: headers : 请求头
    ====================返回======================
    params: code : integer : 0.成功 1.失败
    params: msg : string : 
    params: data : object : 
              vin : string : vin 码
              bandCode : string : 品牌 code
              bandName : string : 品牌 名称
              seriesCode : string : 车系 code
              seriesName : string : 车系 名称
              modelCode : string : 车型code
              modelName : string : 车型名称
              pno18Array : string : PNO18码
              configureCode : string : 配置code
              configureCodeName : string : 配置名称
              interiorCode : string : 内饰code
              interiorCodeName : string : 内饰code
              optionalCodeList : array : 选装code集合
              supportDischarge : integer : 是否支持放电
              supportBluetooth : integer : 是否支持蓝牙
              supportSendToCar : integer : 是否支持发送到车
    """
    _method = "GET"
    _url = "/order/mainOrder/vinCode"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "vin": vin,  # 车辆唯一vin码
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/mainOrder/finish")
def order_mainorder_finish(orderId=None, headers=None, **kwargs):
    """
    订单管理-订单完成-Y
    up_time=1675660618

    params: orderId : string : 
    params: headers : 请求头
    ====================返回======================
    params: code : integer : 0失败1成功
    params: msg : string : 
    params: data : object : 
    """
    _method = "POST"
    _url = "/order/mainOrder/finish"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "orderId": orderId,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/mainOrder/allPriceContent")
def order_mainorder_allpricecontent(orderId=None, headers=None, **kwargs):
    """
    订单管理-查询订单权益接口-Y
    up_time=1675660625

    params: orderId :  : 子订单号 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              userName : string : 联系人姓名
              userMobile : string : 联系人手机号
              orderName : string : 用户昵称,
              orderMobile : string : 用户号码
              allPriceContent : string : 权益内容
    """
    _method = "GET"
    _url = "/order/mainOrder/allPriceContent"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "orderId": orderId,  # 子订单号 
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/mainOrder/getOrderIdByUser")
def order_mainorder_getorderidbyuser(userId=None, headers=None, **kwargs):
    """
    订单管理-通过用户ID查询订单ID-Y
    up_time=1675660638

    params: userId :  : 用户id
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/order/mainOrder/getOrderIdByUser"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户id
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/mainOrder/=getModelNameByOrderId")
def order_mainorder__getmodelnamebyorderid(orderId=None, headers=None, **kwargs):
    """
    订单管理-通过订单号获取车型名称-Y
    up_time=1675660646

    params: orderId :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
    """
    _method = "GET"
    _url = "/order/mainOrder/=getModelNameByOrderId"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "orderId": orderId,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/mainOrder/getCarConfigByOrderId")
def order_mainorder_getcarconfigbyorderid(orderId=None, headers=None, **kwargs):
    """
    订单管理-通过订单号获取配置信息-Y
    up_time=1675660654

    params: orderId :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              salesVersion : string : 销售版本
              appearanceColor : string : 外观颜色
              processColor : string : 套色
              interiorColor : string : 内饰颜色
    """
    _method = "GET"
    _url = "/order/mainOrder/getCarConfigByOrderId"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "orderId": orderId,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/mainOrder/syncScrmExtOrder")
def order_mainorder_syncscrmextorder(modelCode=None, customerCtCode=None, ossId=None, dealerCode=None, scUid=None, unitTaxNo=None, chargePointEquity=None, customerType=None, seriesCode=None, lifetimeWarrantyPrice=None, createTime=None, syncMsg=None, unitInvoiceTitle=None, trimCode=None, phone=None, colorCode=None, soNo=None, syncStatus=None, isArrived=None, orderNo=None, isTestDrive=None, custCertNo=None, configCode=None, VIN=None, potentialName=None, optionCode=None, soStatus=None, orderAllAmount=None, customerId=None, unitName=None, scUname=None, isLifetimeWarranty=None, orderId=None, updateTime=None, deliveryData=None, headers=None, **kwargs):
    """
    SCRM第三方订单同步信息-Y
    up_time=1675406887

    params: ossId : string : 主键
    params: dealerCode : string : 经销商代码
    params: customerId : number : 潜客 ID
    params: isArrived : string : 是否到店（true or false）
    params: isTestDrive : string : 是否试乘试驾（true or false）
    params: orderNo : string : 预订单单号
    params: orderId : number : 预订单订单 ID
    params: soNo : string : DMS 订单编号
    params: soStatus : string : 订单状态
    params: scUid : string : 销售顾问 ID
    params: scUname : string : 销售顾问姓名
    params: VIN : string : 车架号
    params: deliveryData : string : 承诺交车日期
    params: seriesCode : string : 车系代码
    params: modelCode : string : 车型代码
    params: configCode : string : 配置代码
    params: colorCode : string : 外观代码
    params: trimCode : string : 内饰代码
    params: optionCode : string : 选装包
    params: orderAllAmount : number : 订单价格(保留 3 位小数)
    params: customerType : string : 同步个人和企业
    params: potentialName : string : DMS 订单客户手机号
    params: phone : integer : DMS 订单客户证件类型
    params: customerCtCode : string : 证件号码
    params: custCertNo : string : 企业发票抬头
    params: unitName : string : 企业名称
    params: unitInvoiceTitle : string : 企业发票抬头
    params: unitTaxNo : integer : 企业税号
    params: chargePointEquity : integer : 充电桩权益      * 30471001: 7KW 充电桩      * 30471002: 11KW 充电桩      * 30471003: 家充桩置换公充权益      * 30471004:无电车权益
    params: isLifetimeWarranty : integer : (10041001 是, 10041002 否)
    params: lifetimeWarrantyPrice : string : 终身质保价格(保留 2 位小数)
    params: createTime : string : 创建订单时间
    params: updateTime : string : 更新订单时间
    params: syncStatus : integer : 0待同步，1同步成功，2同步失败
    params: syncMsg : string : 同步结果
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0失败1成功
    params: msg : string : 
    params: data : string : 
    """
    _method = "POST"
    _url = "/order/mainOrder/syncScrmExtOrder"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "ossId": ossId,  # 主键
        "dealerCode": dealerCode,  # 经销商代码
        "customerId": customerId,  # 潜客 ID
        "isArrived": isArrived,  # 是否到店（true or false）
        "isTestDrive": isTestDrive,  # 是否试乘试驾（true or false）
        "orderNo": orderNo,  # 预订单单号
        "orderId": orderId,  # 预订单订单 ID
        "soNo": soNo,  # DMS 订单编号
        "soStatus": soStatus,  # 订单状态
        "scUid": scUid,  # 销售顾问 ID
        "scUname": scUname,  # 销售顾问姓名
        "VIN": VIN,  # 车架号
        "deliveryData": deliveryData,  # 承诺交车日期
        "seriesCode": seriesCode,  # 车系代码
        "modelCode": modelCode,  # 车型代码
        "configCode": configCode,  # 配置代码
        "colorCode": colorCode,  # 外观代码
        "trimCode": trimCode,  # 内饰代码
        "optionCode": optionCode,  # 选装包
        "orderAllAmount": orderAllAmount,  # 订单价格(保留 3 位小数)
        "customerType": customerType,  # 同步个人和企业
        "potentialName": potentialName,  # DMS 订单客户手机号
        "phone": phone,  # DMS 订单客户证件类型
        "customerCtCode": customerCtCode,  # 证件号码
        "custCertNo": custCertNo,  # 企业发票抬头
        "unitName": unitName,  # 企业名称
        "unitInvoiceTitle": unitInvoiceTitle,  # 企业发票抬头
        "unitTaxNo": unitTaxNo,  # 企业税号
        "chargePointEquity": chargePointEquity,  # 充电桩权益      * 30471001: 7KW 充电桩      * 30471002: 11KW 充电桩      * 30471003: 家充桩置换公充权益      * 30471004:无电车权益
        "isLifetimeWarranty": isLifetimeWarranty,  # (10041001 是, 10041002 否)
        "lifetimeWarrantyPrice": lifetimeWarrantyPrice,  # 终身质保价格(保留 2 位小数)
        "createTime": createTime,  # 创建订单时间
        "updateTime": updateTime,  # 更新订单时间
        "syncStatus": syncStatus,  # 0待同步，1同步成功，2同步失败
        "syncMsg": syncMsg,  # 同步结果
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/order/mainOrder/informOrder")
def order_mainorder_informorder(sourceInfo=None, systemCode=None, headers=None, **kwargs):
    """
     SCRM第三方转派经销商通知APP同步日志-Y
    up_time=1675407343

    params: sourceInfo : array : 批量操作
              orderId : string : 订单ID
              customerId : number : 潜客ID
              dealerCode : string : 经销商代码(变更后的经销商)
              orderNo : number : 预订单单号
              soNo : string : DMS订单编号
              soStatus : string : 订单状态
              scUid : string : 销售顾问ID
              scUname : string : 销售顾问姓名
    params: systemCode : string : 变更系统
    params: headers : 请求头
    ====================返回======================
    params: code : integer : 0失败1成功
    params: msg : string : 
    params: data : string : 
    """
    _method = "POST"
    _url = "/order/mainOrder/informOrder"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "sourceInfo": sourceInfo,  # 批量操作
        "systemCode": systemCode,  # 变更系统
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


