import allure

from service.app_a import unit_request
from service.app_a.sqls.content.sqls_content_subjectweb import SqlsContentSubjectweb


class AssertsContentSubjectweb(SqlsContentSubjectweb):
    @allure.step(title="接口返回结果校验")
    def assert_content_subjectweb_detailessay(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_subjectweb_detailessay(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["subjectId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_subjectweb_add(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_subjectweb_add(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["isService", "isSearch", "subPicUrl", "subjectName", "explain", "parentId", "web", "status", "level", "siftFlag", "recommend", "serial", "subjectRank", "type", "siftPicUrl"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_subjectweb_treelist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_subjectweb_treelist(**kwargs)
        # flag = self.compare_json_list(self.res, out, [])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_subjectweb_save(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_subjectweb_save(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["delFlag", "isService", "isSearch", "subPicUrl", "subjectName", "explain", "parentId", "status", "siftFlag", "subjectId", "type"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_subjectweb_del(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_subjectweb_del(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["subjectId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_subjectweb_detail(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_subjectweb_detail(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["subjectId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_subjectweb_detailessaynew(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_subjectweb_detailessaynew(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["subjectId"])
        # assert flag, "数据比较不一致"

