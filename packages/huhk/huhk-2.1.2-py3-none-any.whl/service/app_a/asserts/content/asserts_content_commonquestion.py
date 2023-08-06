import allure

from service.app_a import unit_request
from service.app_a.sqls.content.sqls_content_commonquestion import SqlsContentCommonquestion


class AssertsContentCommonquestion(SqlsContentCommonquestion):
    @allure.step(title="接口返回结果校验")
    def assert_content_commonquestion_updatestatus(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_commonquestion_updatestatus(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["essayId", "status"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_commonquestion_update(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_commonquestion_update(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["content", "essayId", "title"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_commonquestion_updaterank(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_commonquestion_updaterank(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["essayId", "rank"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_commonquestion_delete(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_commonquestion_delete(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["essayId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_commonquestion_list(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_commonquestion_list(**kwargs)
        # flag = self.compare_json_list(self.res, out, [])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_commonquestion_publishlist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_commonquestion_publishlist(**kwargs)
        # flag = self.compare_json_list(self.res, out, [])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_commonquestion_add(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_commonquestion_add(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["content", "essayId", "title"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_commonquestion_createid(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_commonquestion_createid(**kwargs)
        # flag = self.compare_json_list(self.res, out, [])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_commonquestion_info(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_commonquestion_info(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["essayId"])
        # assert flag, "数据比较不一致"

