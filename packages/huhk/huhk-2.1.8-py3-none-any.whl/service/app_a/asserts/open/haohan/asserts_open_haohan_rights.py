import allure

from service.app_a import unit_request
from service.app_a.sqls.open.haohan.sqls_open_haohan_rights import SqlsOpenHaohanRights


class AssertsOpenHaohanRights(SqlsOpenHaohanRights):
    @allure.step(title="接口返回结果校验")
    def assert_open_haohan_rights_update(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_open_haohan_rights_update(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["params"])
        # assert flag, "数据比较不一致"

