import allure

from service.app_a import unit_request
from service.app_a.sqls.common.sqls_common_user4c import SqlsCommonUser4C


class AssertsCommonUser4C(SqlsCommonUser4C):
    @allure.step(title="接口返回结果校验")
    def assert_common_user4c_queryactivitysource(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_user4c_queryactivitysource(**kwargs)
        # flag = self.compare_json_list(self.res, out, [])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_common_user4c_page(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_user4c_page(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["lastLoginTimeEnd", "userId", "regisTimeBegin", "userSystemSource", "nickName", "activitySource", "status", "mobile", "createTimeEnd", "memberSystemSource", "createTimeStart", "regisTimeEnd", "ownerFlag", "type", "lastLoginTimeStart"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_common_user4c_vehicleinfo(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_user4c_vehicleinfo(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["mobile", "userId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_common_user4c_getbyid(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_user4c_getbyid(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_common_user4c_updateuser(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_user4c_updateuser(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_common_user4c_download(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_user4c_download(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userIds", "lastLoginTimeEnd", "userId", "regisTimeBegin", "userSystemSource", "downloadType", "nickName", "activitySource", "status", "mobile", "createTimeEnd", "memberSystemSource", "createTimeStart", "regisTimeEnd", "ownerFlag", "type", "lastLoginTimeStart"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_common_user4c_beforepointsexport(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_user4c_beforepointsexport(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userIds", "lastLoginTimeEnd", "userId", "regisTimeBegin", "userSystemSource", "downloadType", "nickName", "activitySource", "status", "mobile", "createTimeEnd", "memberSystemSource", "createTimeStart", "regisTimeEnd", "ownerFlag", "type", "lastLoginTimeStart"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_common_user4c_insert(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_user4c_insert(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["nickName", "avatarUrl", "explain"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_common_user4c_editstatus(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_user4c_editstatus(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId", "status"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_common_user4c_auditexport(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_user4c_auditexport(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userIds", "userId", "userLabel", "downloadType", "nickName", "phone", "registerType", "ownerFlag", "userType"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_common_user4c_identity(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_user4c_identity(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_common_user4c_updateaudit(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_user4c_updateaudit(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId", "auditType"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_common_user4c_auditlist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_user4c_auditlist(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId", "checkStatus", "nickName", "pageNum", "mobile", "registerType", "userName"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_common_user4c_getuserpoints(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_common_user4c_getuserpoints(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        # assert flag, "数据比较不一致"

