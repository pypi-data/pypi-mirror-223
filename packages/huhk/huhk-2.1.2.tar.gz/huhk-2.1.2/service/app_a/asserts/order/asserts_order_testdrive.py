import allure

from service.app_a import unit_request
from service.app_a.sqls.order.sqls_order_testdrive import SqlsOrderTestdrive


class AssertsOrderTestdrive(SqlsOrderTestdrive):
    @allure.step(title="接口返回结果校验")
    def assert_order_testdrive_exportlist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_order_testdrive_exportlist(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["id", "shopName", "createTime", "createByName", "channel", "startTime", "endTime", "phoneNumber"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_order_testdrive_userlist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_order_testdrive_userlist(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["createBy", "modelId"])
        # assert flag, "数据比较不一致"

