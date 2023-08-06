import allure

from service.app_a import unit_request
from service.app_a.sqls.sqls_testdrive import SqlsTestdrive


class AssertsTestdrive(SqlsTestdrive):
    @allure.step(title="接口返回结果校验")
    def assert_testdrive_subscribe(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_testdrive_subscribe(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["appointmentTime", "customerName", "modelId", "shopId", "channel", "leadSanSourceCode", "leadSourceCode", "shopName", "model", "activityCode", "phoneNumber"])
        # assert flag, "数据比较不一致"

