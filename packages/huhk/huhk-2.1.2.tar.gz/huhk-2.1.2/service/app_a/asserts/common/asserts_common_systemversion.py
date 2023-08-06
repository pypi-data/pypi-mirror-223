import allure

from service.app_a import unit_request
from service.app_a.sqls.common.sqls_common_systemversion import SqlsCommonSystemversion


class AssertsCommonSystemversion(SqlsCommonSystemversion):
    @allure.step(title="接口返回结果校验")
    def assert_common_systemversion_save(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_systemversion_save(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["remark", "content", "downloadUrl", "force", "publishStatus", "version", "versionId", "classify", "name"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_common_systemversion_page(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_systemversion_page(**kwargs)
        # flag = self.compare_json_list(self.res, out, [])
        # assert flag, "数据比较不一致"

