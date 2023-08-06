import allure

from service.app_a import unit_request
from service.app_a.sqls.radarpoints.sqls_radarpoints_pointstask import SqlsRadarpointsPointstask


class AssertsRadarpointsPointstask(SqlsRadarpointsPointstask):
    @allure.step(title="接口返回结果校验")
    def assert_radarpoints_pointstask_pagelist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_radarpoints_pointstask_pagelist(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["pointsTaskDateSort", "dateLast", "pointsConfigCode", "pointsConfigName", "mobile", "getPointsQtySort", "dateBegin"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_radarpoints_pointstask_export(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_radarpoints_pointstask_export(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["pointsTaskDateSort", "dateLast", "pointsConfigCode", "pointsConfigName", "mobile", "getPointsQtySort", "dateBegin"])
        # assert flag, "数据比较不一致"

