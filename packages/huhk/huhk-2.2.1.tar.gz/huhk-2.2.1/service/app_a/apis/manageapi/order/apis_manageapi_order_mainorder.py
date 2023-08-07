import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/manageapi/order/mainOrder/pageList")
def manageapi_order_mainorder_pagelist(provinceId=None, orderStatus=None, orderType=None, extOrderStatus=None, modelId=None, current=None, createEndTime=None, channel=None, dealerCode=None, createStartTime=None, mobile=None, cityId=None, mainOrderId=None, orderId=None, extNum=None, userName=None, size=None, headers=None, **kwargs):
    """
    订单管理-后台查询订单列表-Y
    up_time=1675752735

    params: mobile :  : 购买人手机号
    params: userName :  : 购买人
    params: modelId :  : 车型ID
    params: provinceId :  : 省编码
    params: cityId :  : 市编码
    params: orderId :  : 从新增大定逻辑开始，该字段定义为子订单号
     * * 小订转大定时，前端需要通过这个子订单号小订转大定
    params: mainOrderId :  : 主订单号
    params: orderStatus :  : 订单状态
    params: extOrderStatus :  : 第三方订单状态
    params: dealerCode :  : 经销商ID
    params: orderType :  : 订单类型
    params: channel :  : 渠道id 1 app 2 小程序 3 官网
    params: createStartTime :  : 订单创建开始日期
    params: createEndTime :  : 订单创建结束日期
    params: extNum :  : 三方订单号
    params: current :  : 
    params: size :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : integer :  0.成功 1.失败
    params: msg : string : 
    params: data : object : 
              records : array : 
              total : number : 
              size : number : 
              current : number : 
              orders : array : 
              optimizeCountSql : boolean : 
              searchCount : boolean : 
              countId : string : 
              maxLimit : string : 
              pages : number : 
    """
    _method = "GET"
    _url = "/manageapi/order/mainOrder/pageList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "mobile": mobile,  # 购买人手机号
        "userName": userName,  # 购买人
        "modelId": modelId,  # 车型ID
        "provinceId": provinceId,  # 省编码
        "cityId": cityId,  # 市编码
        "orderId": orderId,  # 从新增大定逻辑开始，该字段定义为子订单号      * * 小订转大定时，前端需要通过这个子订单号小订转大定
        "mainOrderId": mainOrderId,  # 主订单号
        "orderStatus": orderStatus,  # 订单状态
        "extOrderStatus": extOrderStatus,  # 第三方订单状态
        "dealerCode": dealerCode,  # 经销商ID
        "orderType": orderType,  # 订单类型
        "channel": channel,  # 渠道id 1 app 2 小程序 3 官网
        "createStartTime": createStartTime,  # 订单创建开始日期
        "createEndTime": createEndTime,  # 订单创建结束日期
        "extNum": extNum,  # 三方订单号
        "current": current,
        "size": size,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/manageapi/order/mainOrder/detail")
def manageapi_order_mainorder_detail(orderId=None, headers=None, **kwargs):
    """
    订单管理-大订订单详情-Y
    up_time=1684999454

    params: orderId :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              sortItems : null : 
              createStartTime : null : 
              createEndTime : null : 
              userId : string : 
              orderId : string : 
              orderStatus : string : 
              orderStatusName : string : 
              createTime : string : 
              userName : string : 
              mobile : string : 
              linkmanMobile : string : 
              originMobile : string : 
              prePrice : null : 
              totalPrice : string : 
              referencePrice : string : 参考价
              discountRightsList : array : 折扣权益列表
              provinceId : string : 
              provinceName : string : 
              cityId : string : 
              cityName : string : 
              orderType : string : 
              orderTypeName : string : 
              modelId : string : 
              modelSnapshotId : null : 
              existFreeOrder : string : 
              existFreeOrderName : string : 
              goodsTotal : number : 
              orderProcess : array : 
              prePricePosterImageUrl : string : 
              modelName : string : 
              depositPriceContent : string : 
              prePriceContent : null : 
              freePriceContent : string : 
              freePriceAttachText : null : 
              delFlag : string : 
              preStartTime : string : 
              preEndTime : string : 
              preToDepositStartTime : string : 
              preToDepositEndTime : string : 
              depositStartTime : string : 
              depositEndTime : string : 
              payTime : null : 
              refundTime : null : 
              payType : null : 
              channel : string : 
              channelName : string : 
              createShowTime : null : 
              payShowTime : null : 
              refundShowTime : null : 
              refundMemo : null : 
              orderPayInfo : object : 
              orderRefundInfo : object : 订单退款信息
              version : null : 
              referrerCode : null : 
              purchaseType : string : 
              certTypeCode : string : 
              certTypeName : string : 
              certNo : string : 
              enterpriseName : string : 
              enterpriseTaxNo : string : 
              depositPrice : string : 
              payMethod : string : 
              isPreToDepositOrder : string : 
              dealerCode : string : 
              dealerName : string : 
              dealerHotLink : string : 
              wishId : null : 
              userOrderStatus : string : 
              userOrderStatusName : string : 
              extOrderStatus : null : 
              extNum : null : 
              extOrderStatusName : null : 
              subCreateTime : null : 
              configureList : array : 
              mainOrderId : string : 
              deliveryDate : null : 
              ownerBy : null : 
              ownerMobile : null : 
              carModel : object : 
              withinPreToDepositTime : null : 
              chargePointEquity : null : 
              chargePointEquityStr : null : 
              needShowApplyForChargingPile : null : 
              latestPrice : string : 
              associatedOrder : null : 
              assPreOrderId : null : 
              assDepositOrderId : null : 
              showPrice : null : 
              carOwnerInfoVo : object : 
              vin : null : 
              depositOrderPolicyContent : string : 
              chargeRightsInfoList : array : 
              rightsOrderVo : null : 
              chargeRightsName : null : 
              refundStatus : null : 
              refundStatusName : null : 
              orderRefundTaskVo : object : 
              orderRefundBillVo : object : 
              dealerCodeFront : null : 
              dealerCodeQueen : null : 
              changeTime : null : 
              systemCode : null : 
    """
    _method = "GET"
    _url = "/manageapi/order/mainOrder/detail"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "orderId": orderId,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


