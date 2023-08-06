import allure

from service.app_a.asserts.order.mainorder.asserts_order_mainorder_scrm2app import AssertsOrderMainorderScrm2App
from service.app_a.apis.order.mainorder import apis_order_mainorder_scrm2app


class FunsOrderMainorderScrm2App(AssertsOrderMainorderScrm2App):
    @allure.step(title="订单管理-订单退款-Y")
    def order_mainorder_scrm2app_refundauditnotice(self, orderMainId="$None$", orderSubId="$None$", status="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/order/mainOrder/scrm2app/refundAuditNotice
                params: orderMainId : string :
                params: orderSubId : string :
                params: status : integer :
                params: headers : 请求头
        """
        orderMainId = self.get_value_choice(orderMainId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        orderSubId = self.get_value_choice(orderSubId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        status = self.get_value_choice(status, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_mainorder_scrm2app.order_mainorder_scrm2app_refundauditnotice(**_kwargs)

        self.assert_order_mainorder_scrm2app_refundauditnotice(_assert, **_kwargs)
        self.set_value(_kwargs)


