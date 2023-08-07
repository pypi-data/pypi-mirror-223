import allure

from service.app_a import unit_request
from service.app_a.sqls.content.sqls_content_subject import SqlsContentSubject


class AssertsContentSubject(SqlsContentSubject):
    @allure.step(title="接口返回结果校验")
    def assert_content_subject_detailessay(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_subject_detailessay(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["subjectId", "subjectName"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_subject_add(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_subject_add(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["level", "parentId", "subPicUrl", "explain", "subjectName", "status", "type"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_subject_del(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_subject_del(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["subjectId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_subject_mobilesubject(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_subject_mobilesubject(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["subjectId", "serial", "parentId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_subject_getessaysubjects(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_subject_getessaysubjects(**kwargs)
        # flag = self.compare_json_list(self.res, out, [])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_subject_detail(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_subject_detail(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["subjectId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_subject_treelist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_subject_treelist(**kwargs)
        # flag = self.compare_json_list(self.res, out, [])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_subject_save(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_subject_save(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["subjectId", "siftFlag", "delFlag", "level", "parentId", "subPicUrl", "isService", "explain", "isSearch", "subjectName", "status", "type"])
        # assert flag, "数据比较不一致"

