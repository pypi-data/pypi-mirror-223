import allure

from service.app_a import unit_request
from service.app_a.sqls.content.sqls_content_contentmanager import SqlsContentContentmanager


class AssertsContentContentmanager(SqlsContentContentmanager):
    @allure.step(title="接口返回结果校验")
    def assert_content_contentmanager_commentlist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_contentmanager_commentlist(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["contentId"])
        # assert flag, "数据比较不一致"

