import allure

from service.app_a import unit_request
from service.app_a.sqls.content.sqls_content_activitymanager import SqlsContentActivitymanager


class AssertsContentActivitymanager(SqlsContentActivitymanager):
    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_updateperson(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_updateperson(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["needLimitPeople", "limitPeople", "activityId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_updateenrolltime(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_updateenrolltime(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["enrollStartTime", "enrollTime", "activityId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_page(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_page(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["target", "city", "activityId", "province", "endTime", "pushTimeSort", "title", "status", "activityTimeSort", "beginTime", "createTimeSort"])
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
        # flag = self.compare_json_list(self.res, out, ["topFlag", "activityId"])
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
        # flag = self.compare_json_list(self.res, out, ["reason", "endTime", "enrollStartTime", "county", "content", "limitPeople", "beginTime", "activityAddr", "agreementId", "coordinate", "publishType", "title", "status", "customerGroup", "activityPicUrl", "needLimitPeople", "activityId", "province", "activityPicURL", "enrollTime", "needArea", "city", "authId", "publishTime"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_update(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_update(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["reason", "endTime", "enrollStartTime", "county", "content", "limitPeople", "beginTime", "activityAddr", "coordinate", "publishType", "title", "status", "customerGroup", "activityPicUrl", "needLimitPeople", "activityId", "province", "activityPicURL", "enrollTime", "city", "needArea", "authId", "publishTime"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_publishupdate(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_publishupdate(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["activityId", "status", "publishStatus", "activityIds"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_statusupdate(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_statusupdate(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["activityIds", "checkStatus"])
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
        # flag = self.compare_json_list(self.res, out, ["target", "city", "activityId", "province", "endTime", "pushTimeSort", "title", "status", "activityTimeSort", "beginTime", "createTimeSort"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_activitymanager_listlog(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_activitymanager_listlog(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["activityId"])
        # assert flag, "数据比较不一致"

