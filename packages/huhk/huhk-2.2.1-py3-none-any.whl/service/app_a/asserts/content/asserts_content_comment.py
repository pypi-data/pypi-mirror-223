import allure

from service.app_a import unit_request
from service.app_a.sqls.content.sqls_content_comment import SqlsContentComment


class AssertsContentComment(SqlsContentComment):
    @allure.step(title="接口返回结果校验")
    def assert_content_comment_updatestatus(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_comment_updatestatus(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["commentId", "fromStatus", "toStatus", "commentType"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_comment_download(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_comment_download(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["downloadType", "nickName", "status", "mobile", "keyWord", "contentCommentIds", "startTime", "endTime", "EssayCommentIds"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_comment_commenttop(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_comment_commenttop(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["commentId", "topFlag", "commentType"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_comment_list(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_comment_list(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["commentType", "nickName", "checkedStatus", "mobile", "keyWord", "essayId", "startTime", "endTime"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_comment_delete(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_comment_delete(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["commentId", "toStatus", "commentType"])
        # assert flag, "数据比较不一致"

