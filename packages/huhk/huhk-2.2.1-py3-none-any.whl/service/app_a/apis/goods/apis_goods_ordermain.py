import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/goods/orderMain/pay")
def goods_ordermain_pay(orderMainId=None, headers=None, **kwargs):
    """
    已提车按钮接口-Y
    up_time=1675328427

    params: orderMainId : text : 订单id
    params: headers : 请求头
    ====================返回======================
    """
    _method = "POST"
    _url = "/goods/orderMain/pay"

    _headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    _headers.update({"headers": headers})

    _data = {
        "orderMainId": orderMainId,  # 订单id
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/orderMain/orderExports")
def goods_ordermain_orderexports(endTime=None, userMobile=None, testDriveIdStr=None, billStatus	=None, exportType=None, shopName=None, startTime=None, modelName=None, userName=None, headers=None, **kwargs):
    """
    订单列表文件导出接口-Y
    up_time=1675660544

    params: userMobile :  : 手机号
    params: userName :  : 用户名
    params: shopName :  : 店名
    params: modelName :  : 车型
    params: billStatus	 :  : 支付状态
    params: startTime :  : 开始时间
    params: endTime :  : 结束时间
    params: exportType :  : 导出类型
    params: testDriveIdStr :  : 订单集合字符串
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/goods/orderMain/orderExports"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userMobile": userMobile,  # 手机号
        "userName": userName,  # 用户名
        "shopName": shopName,  # 店名
        "modelName": modelName,  # 车型
        "billStatus	": billStatus	,  # 支付状态
        "startTime": startTime,  # 开始时间
        "endTime": endTime,  # 结束时间
        "exportType": exportType,  # 导出类型
        "testDriveIdStr": testDriveIdStr,  # 订单集合字符串
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/orderMain/getOrderMainPage")
def goods_ordermain_getordermainpage(shopName=None, userMobile=None, startTime=None, endTime=None, modelName=None, orderStatus	=None, userName=None, headers=None, **kwargs):
    """
    订单查询接口-Y
    up_time=1675660564

    params: userMobile :  : 手机号
    params: userName :  : 用户名
    params: modelName :  : 车型
    params: orderStatus	 :  : 支付状态 1001待支付 1002已支付 1003已完成 1004待退款
1005已取消 1006已退款 1007已驳回
    params: startTime :  : 开始时间
    params: endTime :  : 结束时间
    params: shopName :  : 门店名称
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功
    params: msg : string : 描述
    params: data : object : 返回
              records : array : 小订订单集合
              maxLimit : number : 待退款角标
              total : number : 总行数
              size : number : 每页数
              current : number : 当前页
              pages : number : 
    """
    _method = "GET"
    _url = "/goods/orderMain/getOrderMainPage"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userMobile": userMobile,  # 手机号
        "userName": userName,  # 用户名
        "modelName": modelName,  # 车型
        "orderStatus	": orderStatus	,  # 支付状态 1001待支付 1002已支付 1003已完成 1004待退款 1005已取消 1006已退款 1007已驳回
        "startTime": startTime,  # 开始时间
        "endTime": endTime,  # 结束时间
        "shopName": shopName,  # 门店名称
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/orderMain/getOrderMainById")
def goods_ordermain_getordermainbyid(orderMainId=None, headers=None, **kwargs):
    """
    订单详情查询-Y
    up_time=1675660571

    params: orderMainId :  : 订单id
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              orderMainId : number : 订单id
              channelId : number : 渠道id
              orderType : string : 订单类型
              userId : number : 用户id
              userName : string : 用户名
              userMobile : string : 手机号
              createTime : string : 创建时间
              customerName : null : 客户名
              userType : null : 用户类型
              phone : null : 客户手机号
              areaName : string : 上牌城市
              shopId : number : 网点id
              shopName : string : 网点名称
              shopAddress : string : 网点地址
              modelId : number : 车型id
              modelName : string : 车型名称
              configurationAndOptions : string : 选装与配置
              totalPrice : number : 购车总价
              prePrice : number : 定金
              payType : number : 支付方式1：微信支付 2:支付宝支付
              payTime : string : 支付时间
              billStatus : number : 单据状态0：待支付 1：支付成功 2：支付失败
              avatar : null : 头像
    """
    _method = "GET"
    _url = "/goods/orderMain/getOrderMainById"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "orderMainId": orderMainId,  # 订单id
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


