import allure

from service.app_a import unit_request
from service.app_a.sqls.order.sqls_order_order import SqlsOrderOrder


class AssertsOrderOrder(SqlsOrderOrder):
    @allure.step(title="接口返回结果校验")
    def assert_order_order_orderdetail(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_order_order_orderdetail(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId", "orderStatus", "total", "pageNum", "orderId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_order_order_finish(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_order_order_finish(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["orderId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_order_order_refundreject(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_order_order_refundreject(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["orderId"])
        # assert flag, "数据比较不一致"

