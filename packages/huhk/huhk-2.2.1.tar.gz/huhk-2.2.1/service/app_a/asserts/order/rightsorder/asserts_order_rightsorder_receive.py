import allure

from service.app_a import unit_request
from service.app_a.sqls.order.rightsorder.sqls_order_rightsorder_receive import SqlsOrderRightsorderReceive


class AssertsOrderRightsorderReceive(SqlsOrderRightsorderReceive):
    @allure.step(title="接口返回结果校验")
    def assert_order_rightsorder_receive_update(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_order_rightsorder_receive_update(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["orderMainId", "userId", "rightsId", "createBy", "payDate", "createTime", "refundDate", "payBillNo", "useStatus", "rightsType", "rightsName", "payAmount", "mobile", "receiveDate", "refundBillNo", "updateId", "updateTime", "rightsOrderId"])
        # assert flag, "数据比较不一致"

