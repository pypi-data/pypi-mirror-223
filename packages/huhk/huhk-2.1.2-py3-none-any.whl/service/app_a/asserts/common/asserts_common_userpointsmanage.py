import allure

from service.app_a import unit_request
from service.app_a.sqls.common.sqls_common_userpointsmanage import SqlsCommonUserpointsmanage


class AssertsCommonUserpointsmanage(SqlsCommonUserpointsmanage):
    @allure.step(title="接口返回结果校验")
    def assert_common_userpointsmanage_userpointsexport(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_userpointsmanage_userpointsexport(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["nickName", "beginTime", "mobile", "logIds", "endTime"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_common_userpointsmanage_page(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_userpointsmanage_page(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["nickName", "mobile", "endTime", "beginTime"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_common_userpointsmanage_manualchangeuserpoints(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_userpointsmanage_manualchangeuserpoints(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId", "operateMark", "operatePoint", "pointChangType", "taskName", "operateType"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_common_userpointsmanage_beforepointsexport(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_userpointsmanage_beforepointsexport(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["nickName", "beginTime", "mobile", "logIds", "endTime"])
        # assert flag, "数据比较不一致"

