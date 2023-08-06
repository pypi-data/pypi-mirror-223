import allure

from service.app_a.asserts.radarpoints.userpoints.asserts_radarpoints_userpoints_exchangeinfo import AssertsRadarpointsUserpointsExchangeinfo
from service.app_a.apis.radarpoints.userpoints import apis_radarpoints_userpoints_exchangeinfo


class FunsRadarpointsUserpointsExchangeinfo(AssertsRadarpointsUserpointsExchangeinfo):
    @allure.step(title="用户中心-兑换明细 - 分页查询")
    def radarpoints_userpoints_exchangeinfo_pagelist(self, userId="$None$", orderEndTime="$None$", consigneeName="$None$", current=1, goodsOrderId="$None$", orderStartTime="$None$", mobile="$None$", size=10, _assert=True,  **kwargs):
        """
            url=/radarpoints/userPoints/exchangeInfo/pageList
                params: size :  : 每页大小
                params: current :  : 当前页
                params: consigneeName :  : 收货人姓名
                params: goodsOrderId :  : 商品订单
                params: mobile :  : 收货人电话
                params: orderStartTime :  : 下单开始时间
                params: orderEndTime :  : 下单结束时间
                params: headers : 请求头
        """
        userId = self.get_list_choice(userId, list_or_dict=None, key="userId")
        orderEndTime = self.get_list_choice(orderEndTime, list_or_dict=None, key="orderEndTime")
        consigneeName = self.get_list_choice(consigneeName, list_or_dict=None, key="consigneeName")
        goodsOrderId = self.get_list_choice(goodsOrderId, list_or_dict=None, key="goodsOrderId")
        orderStartTime = self.get_list_choice(orderStartTime, list_or_dict=None, key="orderStartTime")
        mobile = self.get_list_choice(mobile, list_or_dict=None, key="mobile")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_radarpoints_userpoints_exchangeinfo.radarpoints_userpoints_exchangeinfo_pagelist(**_kwargs)

        self.assert_radarpoints_userpoints_exchangeinfo_pagelist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


