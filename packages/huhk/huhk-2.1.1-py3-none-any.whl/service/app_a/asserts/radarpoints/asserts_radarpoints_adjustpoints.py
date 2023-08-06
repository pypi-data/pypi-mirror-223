import allure

from service.app_a import unit_request
from service.app_a.sqls.radarpoints.sqls_radarpoints_adjustpoints import SqlsRadarpointsAdjustpoints


class AssertsRadarpointsAdjustpoints(SqlsRadarpointsAdjustpoints):
    @allure.step(title="接口返回结果校验")
    def assert_radarpoints_adjustpoints_pagelist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_radarpoints_adjustpoints_pagelist(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId", "nickName", "optAbilityName", "adjustTimeEnd", "mobile", "adjustNotes", "optAbility", "adjustTimeBefore"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_radarpoints_adjustpoints_getuserpointsqtybyuserid(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_radarpoints_adjustpoints_getuserpointsqtybyuserid(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_radarpoints_adjustpoints_getuserpointsqtybymobile(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_radarpoints_adjustpoints_getuserpointsqtybymobile(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["mobile"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_radarpoints_adjustpoints_export(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_radarpoints_adjustpoints_export(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId", "nickName", "optAbilityName", "adjustTimeEnd", "mobile", "adjustNotes", "optAbility", "adjustTimeBefore"])
        # assert flag, "数据比较不一致"

