import allure

from service.app_a import unit_request
from service.app_a.sqls.content.sqls_content_question import SqlsContentQuestion


class AssertsContentQuestion(SqlsContentQuestion):
    @allure.step(title="接口返回结果校验")
    def assert_content_question_answerquestion(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_question_answerquestion(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["questionId", "author", "answerContent"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_question_revoke(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_question_revoke(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["questionId", "operaType"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_question_getmanegequestionlist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_question_getmanegequestionlist(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["status", "mobile", "keyWord", "startTime", "endTime"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_question_getbyid(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_question_getbyid(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["questionId"])
        # assert flag, "数据比较不一致"

