import allure

from service.app_a.asserts.order.asserts_order_order import AssertsOrderOrder
from service.app_a.apis.order import apis_order_order


class FunsOrderOrder(AssertsOrderOrder):
    @allure.step(title="订单详情")
    def order_order_orderdetail(self, userId="$None$", orderStatus="$None$", total="$None$", pageSize="$None$", pageNum=1, orderId="$None$", _assert=True,  **kwargs):
        """
            url=/order/order/orderDetail{orderId}{userId}
                params: orderId :  : 订单主单Id
                params: orderStatus : string : 订单状态
                params: pageSize : number : 每页大小
                params: pageNum : number : 当前页
                params: total : number : 总数
                params: headers : 请求头
        """
        userId = self.get_list_choice(userId, list_or_dict=None, key="userId")
        orderStatus = self.get_list_choice(orderStatus, list_or_dict=None, key="orderStatus")
        total = self.get_list_choice(total, list_or_dict=None, key="total")
        pageSize = self.get_list_choice(pageSize, list_or_dict=None, key="pageSize")
        orderId = self.get_list_choice(orderId, list_or_dict=None, key="orderId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_order.order_order_orderdetail(**_kwargs)

        self.assert_order_order_orderdetail(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="订单提车-Y")
    def order_order_finish(self, orderId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/order/order/finish
                params: orderId : string : 主订单ID
                params: headers : 请求头
        """
        orderId = self.get_value_choice(orderId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_order.order_order_finish(**_kwargs)

        self.assert_order_order_finish(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="订单退款驳回-Y")
    def order_order_refundreject(self, orderId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/order/order/refundReject
                params: orderId : string : 主订单ID
                params: headers : 请求头
        """
        orderId = self.get_value_choice(orderId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_order.order_order_refundreject(**_kwargs)

        self.assert_order_order_refundreject(_assert, **_kwargs)
        self.set_value(_kwargs)


