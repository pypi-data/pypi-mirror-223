import allure

from service.app_a.asserts.goods.asserts_goods_ordermain import AssertsGoodsOrdermain
from service.app_a.apis.goods import apis_goods_ordermain


class FunsGoodsOrdermain(AssertsGoodsOrdermain):
    @allure.step(title="已提车按钮接口-Y")
    def goods_ordermain_pay(self, orderMainId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/goods/orderMain/pay
                params: orderMainId : text : 订单id
                params: headers : 请求头
        """
        orderMainId = self.get_value_choice(orderMainId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_ordermain.goods_ordermain_pay(**_kwargs)

        self.assert_goods_ordermain_pay(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="订单列表文件导出接口-Y")
    def goods_ordermain_orderexports(self, endTime="$None$", userMobile="$None$", testDriveIdStr="$None$", billStatus="$None$", exportType="$None$", shopName="$None$", startTime="$None$", modelName="$None$", userName="$None$", _assert=True,  **kwargs):
        """
            url=/goods/orderMain/orderExports
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
        """
        endTime = self.get_list_choice(endTime, list_or_dict=None, key="endTime")
        userMobile = self.get_list_choice(userMobile, list_or_dict=None, key="userMobile")
        testDriveIdStr = self.get_list_choice(testDriveIdStr, list_or_dict=None, key="testDriveIdStr")
        billStatus = self.get_list_choice(billStatus, list_or_dict=None, key="billStatus")
        exportType = self.get_list_choice(exportType, list_or_dict=None, key="exportType")
        shopName = self.get_list_choice(shopName, list_or_dict=None, key="shopName")
        startTime = self.get_list_choice(startTime, list_or_dict=None, key="startTime")
        modelName = self.get_list_choice(modelName, list_or_dict=None, key="modelName")
        userName = self.get_list_choice(userName, list_or_dict=None, key="userName")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_ordermain.goods_ordermain_orderexports(**_kwargs)

        self.assert_goods_ordermain_orderexports(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="订单查询接口-Y")
    def goods_ordermain_getordermainpage(self, shopName="$None$", userMobile="$None$", startTime="$None$", endTime="$None$", modelName="$None$", orderStatus="$None$", userName="$None$", _assert=True,  **kwargs):
        """
            url=/goods/orderMain/getOrderMainPage
                params: userMobile :  : 手机号
                params: userName :  : 用户名
                params: modelName :  : 车型
                params: orderStatus	 :  : 支付状态 1001待支付 1002已支付 1003已完成 1004待退款
                1005已取消 1006已退款 1007已驳回
                params: startTime :  : 开始时间
                params: endTime :  : 结束时间
                params: shopName :  : 门店名称
                params: headers : 请求头
        """
        shopName = self.get_list_choice(shopName, list_or_dict=None, key="shopName")
        userMobile = self.get_list_choice(userMobile, list_or_dict=None, key="userMobile")
        startTime = self.get_list_choice(startTime, list_or_dict=None, key="startTime")
        endTime = self.get_list_choice(endTime, list_or_dict=None, key="endTime")
        modelName = self.get_list_choice(modelName, list_or_dict=None, key="modelName")
        orderStatus = self.get_list_choice(orderStatus, list_or_dict=None, key="orderStatus")
        userName = self.get_list_choice(userName, list_or_dict=None, key="userName")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_ordermain.goods_ordermain_getordermainpage(**_kwargs)

        self.assert_goods_ordermain_getordermainpage(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="订单详情查询-Y")
    def goods_ordermain_getordermainbyid(self, orderMainId="$None$", _assert=True,  **kwargs):
        """
            url=/goods/orderMain/getOrderMainById
                params: orderMainId :  : 订单id
                params: headers : 请求头
        """
        orderMainId = self.get_list_choice(orderMainId, list_or_dict=None, key="orderMainId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_ordermain.goods_ordermain_getordermainbyid(**_kwargs)

        self.assert_goods_ordermain_getordermainbyid(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


