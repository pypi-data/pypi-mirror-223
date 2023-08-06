import allure

from service.app_a import unit_request
from service.app_a.sqls.content.sqls_content_hotsearch import SqlsContentHotsearch


class AssertsContentHotsearch(SqlsContentHotsearch):
    @allure.step(title="接口返回结果校验")
    def assert_content_hotsearch_rank(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_hotsearch_rank(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["kId", "rank"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_hotsearch_list(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_hotsearch_list(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["kId", "rank"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_hotsearch_insert(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_hotsearch_insert(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["keyWord", "point"])
        # assert flag, "数据比较不一致"

