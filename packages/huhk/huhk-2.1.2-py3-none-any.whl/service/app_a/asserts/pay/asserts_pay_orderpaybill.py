import allure

from service.app_a import unit_request
from service.app_a.sqls.pay.sqls_pay_orderpaybill import SqlsPayOrderpaybill


class AssertsPayOrderpaybill(SqlsPayOrderpaybill):
    @allure.step(title="接口返回结果校验")
    def assert_pay_orderpaybill_orderrefund(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_pay_orderpaybill_orderrefund(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["orderMainId"])
        # assert flag, "数据比较不一致"

