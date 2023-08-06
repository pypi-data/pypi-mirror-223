import allure

from service.app_a import unit_request
from service.app_a.sqls.content.sqls_content_essayweb import SqlsContentEssayweb


class AssertsContentEssayweb(SqlsContentEssayweb):
    @allure.step(title="接口返回结果校验")
    def assert_content_essayweb_add(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_essayweb_add(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["essPicUrl", "content", "publishType", "title", "author", "status", "publishTime", "essayId", "publishChannel"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_essayweb_searchbykey(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_essayweb_searchbykey(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["key"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_essayweb_delete_(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_essayweb_delete_(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["essayId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_essayweb_getbyid(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_essayweb_getbyid(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["essayId", "subjectId"])
        # assert flag, "数据比较不一致"

