import allure

from service.app_a import unit_request
from service.app_a.sqls.sqls_essay import SqlsEssay


class AssertsEssay(SqlsEssay):
    @allure.step(title="接口返回结果校验")
    def assert_essay_batch(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_essay_batch(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["essayId", "batchType"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_essay_querylistcount(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_essay_querylistcount(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["author", "status", "essayId", "keyWord", "subjectId", "startTime", "endTime"])
        # assert flag, "数据比较不一致"

