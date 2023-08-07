import allure

from service.app_a import unit_request
from service.app_a.sqls.content.sqls_content_activitymanager import SqlsContentActivitymanager


class AssertsContentActivitymanager(SqlsContentActivitymanager):
    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_updateperson(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_updateperson(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["needLimitPeople", "activityId", "limitPeople"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_updateenrolltime(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_updateenrolltime(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["activityId", "enrollStartTime", "enrollTime"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_page(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_page(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["activityTimeSort", "title", "pushTimeSort", "beginTime", "status", "province", "createTimeSort", "city", "target", "endTime", "activityId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_actinfoupdate(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_actinfoupdate(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["operationType", "activityId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_setactivitysort(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_setactivitysort(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["activityId", "sort"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_getactivityinfo_(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_getactivityinfo_(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["activityId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_activitytop_(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_activitytop_(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["activityId", "topFlag"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_activityjoinuserexport(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_activityjoinuserexport(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["activityId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_save(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_save(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["title", "publishType", "authId", "coordinate", "county", "activityPicUrl", "status", "province", "publishTime", "needLimitPeople", "content", "reason", "activityId", "enrollTime", "activityAddr", "city", "agreementId", "activityPicURL", "needArea", "beginTime", "customerGroup", "endTime", "enrollStartTime", "limitPeople"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_update(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_update(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["title", "publishType", "authId", "coordinate", "county", "activityPicUrl", "status", "province", "publishTime", "content", "needLimitPeople", "reason", "activityId", "enrollTime", "activityAddr", "city", "activityPicURL", "needArea", "beginTime", "customerGroup", "endTime", "enrollStartTime", "limitPeople"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_publishupdate(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_publishupdate(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["activityId", "activityIds", "publishStatus", "status"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_statusupdate(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_statusupdate(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["checkStatus", "activityIds"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_enrollupdate(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_enrollupdate(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["checkEnroll", "activityIds"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_activityexport(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_activityexport(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["activityTimeSort", "title", "pushTimeSort", "beginTime", "status", "province", "createTimeSort", "city", "target", "endTime", "activityId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_listlog(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_listlog(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["activityId"])
        # assert flag, "数据比较不一致"

