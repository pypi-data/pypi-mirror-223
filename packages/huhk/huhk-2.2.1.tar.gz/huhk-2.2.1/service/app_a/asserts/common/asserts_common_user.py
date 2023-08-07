import allure

from service.app_a import unit_request
from service.app_a.sqls.common.sqls_common_user import SqlsCommonUser


class AssertsCommonUser(SqlsCommonUser):
    @allure.step(title="接口返回结果校验")
    def assert_common_user_getuservestlist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_user_getuservestlist(**kwargs)
        # flag = self.compare_json_list(self.res, out, [])
        # assert flag, "数据比较不一致"

