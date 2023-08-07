import allure

from service.app_a import unit_request
from service.app_a.sqls.order.mainorder.sqls_order_mainorder_scrm2app import SqlsOrderMainorderScrm2App


class AssertsOrderMainorderScrm2App(SqlsOrderMainorderScrm2App):
    @allure.step(title="接口返回结果校验")
    def assert_order_mainorder_scrm2app_refundauditnotice(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_order_mainorder_scrm2app_refundauditnotice(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["orderMainId", "orderSubId", "status"])
        # assert flag, "数据比较不一致"

