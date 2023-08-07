import allure

from service.app_a import unit_request
from service.app_a.sqls.admin.sqls_admin_guc import SqlsAdminGuc


class AssertsAdminGuc(SqlsAdminGuc):
    @allure.step(title="接口返回结果校验")
    def assert_admin_guc_guclogout(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_admin_guc_guclogout(**kwargs)
        # flag = self.compare_json_list(self.res, out, [])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_admin_guc_guclogin(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_admin_guc_guclogin(**kwargs)
        # flag = self.compare_json_list(self.res, out, [])
        # assert flag, "数据比较不一致"

