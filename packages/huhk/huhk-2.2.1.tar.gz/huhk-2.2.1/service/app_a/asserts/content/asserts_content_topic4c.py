import allure

from service.app_a import unit_request
from service.app_a.sqls.content.sqls_content_topic4c import SqlsContentTopic4C


class AssertsContentTopic4C(SqlsContentTopic4C):
    @allure.step(title="接口返回结果校验")
    def assert_content_topic4c_del(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_topic4c_del(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["topicId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_topic4c_getcontentlist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_topic4c_getcontentlist(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["topicId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_topic4c_list(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_topic4c_list(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["createBy", "topicId", "keyWord", "startTime", "endTime"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_topic4c_insert(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_topic4c_insert(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["topicId", "author", "topicTitle"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_topic4c_top(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_topic4c_top(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["topicId", "type"])
        # assert flag, "数据比较不一致"

