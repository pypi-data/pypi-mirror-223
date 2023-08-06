import allure

from service.app_a.asserts.pay.asserts_pay_orderpaybill import AssertsPayOrderpaybill
from service.app_a.apis.pay import apis_pay_orderpaybill


class FunsPayOrderpaybill(AssertsPayOrderpaybill):
    @allure.step(title="订单退款接口-Y")
    def pay_orderpaybill_orderrefund(self, orderMainId="$None$", _assert=True,  **kwargs):
        """
            url=/pay/orderpaybill/orderRefund
                params: orderMainId :  : 订单id
                params: headers : 请求头
        """
        orderMainId = self.get_list_choice(orderMainId, list_or_dict=None, key="orderMainId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_pay_orderpaybill.pay_orderpaybill_orderrefund(**_kwargs)

        self.assert_pay_orderpaybill_orderrefund(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


