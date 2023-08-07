import allure

from service.app_a import unit_request
from service.app_a.sqls.content.sqls_content_messagemanager import SqlsContentMessagemanager


class AssertsContentMessagemanager(SqlsContentMessagemanager):
    @allure.step(title="接口返回结果校验")
    def assert_content_messagemanager_page(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_messagemanager_page(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["pStartTime", "userId", "cStartTime", "authId", "endTime", "messageId", "pEndTime", "cEndTime", "content", "status", "beginTime"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_messagemanager_getmessageinfo_(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_messagemanager_getmessageinfo_(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["messageId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_messagemanager_messagetop(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_messagemanager_messagetop(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["topFlag", "messageIds"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_messagemanager_insert(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_messagemanager_insert(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["imageUrl", "sendScope", "messageId", "param", "checkPublish", "sourceType", "publishType", "checkStatus", "content", "publishTime", "type"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_messagemanager_update(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_messagemanager_update(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["imageUrl", "sendScope", "userMobiles", "messageId", "param", "checkPublish", "sourceType", "checkStatus", "content", "type"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_messagemanager_publishupdate(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_messagemanager_publishupdate(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["publishStatus", "messageIds"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_messagemanager_statusupdate(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_messagemanager_statusupdate(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["checkStatus", "messageIds"])
        # assert flag, "数据比较不一致"

