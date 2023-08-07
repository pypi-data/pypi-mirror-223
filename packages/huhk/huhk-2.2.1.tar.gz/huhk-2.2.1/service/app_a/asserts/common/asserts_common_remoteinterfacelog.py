import allure

from service.app_a import unit_request
from service.app_a.sqls.common.sqls_common_remoteinterfacelog import SqlsCommonRemoteinterfacelog


class AssertsCommonRemoteinterfacelog(SqlsCommonRemoteinterfacelog):
    @allure.step(title="接口返回结果校验")
    def assert_common_remoteinterfacelog_getlogpage(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_remoteinterfacelog_getlogpage(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["mobile", "startTime", "endTime", "interfaceType", "userName"])
        # assert flag, "数据比较不一致"

