import allure

from service.app_a import unit_request
from service.app_a.sqls.content.sqls_content_recruit import SqlsContentRecruit


class AssertsContentRecruit(SqlsContentRecruit):
    @allure.step(title="接口返回结果校验")
    def assert_content_recruit_save(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_recruit_save(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["fileName", "fileUrl"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_recruit_detail(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_recruit_detail(**kwargs)
        # flag = self.compare_json_list(self.res, out, [])
        # assert flag, "数据比较不一致"

