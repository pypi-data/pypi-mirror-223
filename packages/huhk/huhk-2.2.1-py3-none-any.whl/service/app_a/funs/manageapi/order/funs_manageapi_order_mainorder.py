import allure

from service.app_a.asserts.manageapi.order.asserts_manageapi_order_mainorder import AssertsManageapiOrderMainorder
from service.app_a.apis.manageapi.order import apis_manageapi_order_mainorder


class FunsManageapiOrderMainorder(AssertsManageapiOrderMainorder):
    @allure.step(title="订单管理-后台查询订单列表-Y")
    def manageapi_order_mainorder_pagelist(self, provinceId="$None$", orderStatus="$None$", orderType="$None$", extOrderStatus="$None$", modelId="$None$", current=1, createEndTime="$None$", channel="$None$", dealerCode="$None$", createStartTime="$None$", mobile="$None$", cityId="$None$", mainOrderId="$None$", orderId="$None$", extNum="$None$", userName="$None$", size=10, _assert=True,  **kwargs):
        """
            url=/manageapi/order/mainOrder/pageList
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
        """
        provinceId = self.get_list_choice(provinceId, list_or_dict=None, key="provinceId")
        orderStatus = self.get_list_choice(orderStatus, list_or_dict=None, key="orderStatus")
        orderType = self.get_list_choice(orderType, list_or_dict=None, key="orderType")
        extOrderStatus = self.get_list_choice(extOrderStatus, list_or_dict=None, key="extOrderStatus")
        modelId = self.get_list_choice(modelId, list_or_dict=None, key="modelId")
        createEndTime = self.get_list_choice(createEndTime, list_or_dict=None, key="createEndTime")
        channel = self.get_list_choice(channel, list_or_dict=None, key="channel")
        dealerCode = self.get_list_choice(dealerCode, list_or_dict=None, key="dealerCode")
        createStartTime = self.get_list_choice(createStartTime, list_or_dict=None, key="createStartTime")
        mobile = self.get_list_choice(mobile, list_or_dict=None, key="mobile")
        cityId = self.get_list_choice(cityId, list_or_dict=None, key="cityId")
        mainOrderId = self.get_list_choice(mainOrderId, list_or_dict=None, key="mainOrderId")
        orderId = self.get_list_choice(orderId, list_or_dict=None, key="orderId")
        extNum = self.get_list_choice(extNum, list_or_dict=None, key="extNum")
        userName = self.get_list_choice(userName, list_or_dict=None, key="userName")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_manageapi_order_mainorder.manageapi_order_mainorder_pagelist(**_kwargs)

        self.assert_manageapi_order_mainorder_pagelist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="订单管理-大订订单详情-Y")
    def manageapi_order_mainorder_detail(self, orderId="$None$", _assert=True,  **kwargs):
        """
            url=/manageapi/order/mainOrder/detail
                params: orderId :  :
                params: headers : 请求头
        """
        orderId = self.get_list_choice(orderId, list_or_dict=None, key="orderId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_manageapi_order_mainorder.manageapi_order_mainorder_detail(**_kwargs)

        self.assert_manageapi_order_mainorder_detail(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


