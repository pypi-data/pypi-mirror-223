import allure

from service.app_a import unit_request
from service.app_a.sqls.order.sqls_order_rightsorder import SqlsOrderRightsorder


class AssertsOrderRightsorder(SqlsOrderRightsorder):
    @allure.step(title="接口返回结果校验")
    def assert_order_rightsorder_export(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_order_rightsorder_export(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["rightsType", "userId", "receiveDateEnd", "orderMainId", "payDateBegin", "receiveDateBegin", "mobile", "payDateEnd", "rightsOrderId", "useStatus"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_order_rightsorder_insert(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_order_rightsorder_insert(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["rightsId", "rightsName", "rightsType", "userId", "refundDate", "createTime", "receiveDate", "refundBillNo", "updateId", "payBillNo", "payDate", "mobile", "payAmount", "createBy", "rightsOrderId", "updateTime", "orderMainId", "useStatus"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_order_rightsorder_page(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_order_rightsorder_page(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["rightsType", "userId", "receiveDateEnd", "orderMainId", "payDateBegin", "receiveDateBegin", "mobile", "payDateEnd", "rightsOrderId", "useStatus"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_order_rightsorder_receive(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_order_rightsorder_receive(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["rightsId", "orderId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_order_rightsorder_getorderlist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_order_rightsorder_getorderlist(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["rightsType", "receiveDate", "rightsNameList", "useStatusList", "mobile", "orderMainId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_order_rightsorder_statusupdate(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_order_rightsorder_statusupdate(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["soNo", "workStatus"])
        # assert flag, "数据比较不一致"

