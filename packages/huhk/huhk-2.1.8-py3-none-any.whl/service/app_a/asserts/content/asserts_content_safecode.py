import allure

from service.app_a import unit_request
from service.app_a.sqls.content.sqls_content_safecode import SqlsContentSafecode


class AssertsContentSafecode(SqlsContentSafecode):
    @allure.step(title="接口返回结果校验")
    def assert_content_safecode_close(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_safecode_close(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["safeCode"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_safecode_add(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_safecode_add(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["safeCode"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_safecode_verify(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_safecode_verify(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["safeCode"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_safecode_getstatus(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_safecode_getstatus(**kwargs)
        # flag = self.compare_json_list(self.res, out, [])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_safecode_reset(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_safecode_reset(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["safeCode"])
        # assert flag, "数据比较不一致"

