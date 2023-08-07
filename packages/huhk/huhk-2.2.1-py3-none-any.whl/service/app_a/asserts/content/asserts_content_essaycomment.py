import allure

from service.app_a import unit_request
from service.app_a.sqls.content.sqls_content_essaycomment import SqlsContentEssaycomment


class AssertsContentEssaycomment(SqlsContentEssaycomment):
    @allure.step(title="接口返回结果校验")
    def assert_content_essaycomment_manageadd(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_essaycomment_manageadd(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["author", "essayId", "parentId", "content"])
        # assert flag, "数据比较不一致"

