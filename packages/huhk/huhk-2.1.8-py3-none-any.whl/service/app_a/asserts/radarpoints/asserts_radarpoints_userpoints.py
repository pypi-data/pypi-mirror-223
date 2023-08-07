import allure

from service.app_a import unit_request
from service.app_a.sqls.radarpoints.sqls_radarpoints_userpoints import SqlsRadarpointsUserpoints


class AssertsRadarpointsUserpoints(SqlsRadarpointsUserpoints):
    @allure.step(title="接口返回结果校验")
    def assert_radarpoints_userpoints_pagelist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_radarpoints_userpoints_pagelist(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["cumulativeConsumptionMost", "userId", "physicalIntegralLeast", "registrationTimeEnd", "freezeQtyLeast", "registrationTimeBegin", "cumulativeAcquisitionMost", "mobile", "cumulativeAcquisitionLeast", "cumulativeConsumptionLeast", "freezeQtyMost", "physicalIntegralMost", "nickName", "conversionFrequencyLeast", "conversionFrequencyMost"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_radarpoints_userpoints_export(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_radarpoints_userpoints_export(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["cumulativeConsumptionMost", "physicalIntegralLeast", "registrationTimeEnd", "registrationTimeBegin", "cumulativeAcquisitionMost", "cumulativeAcquisitionLeast", "cumulativeConsumptionLeast", "physicalIntegralMost", "nickName", "conversionFrequencyLeast", "conversionFrequencyMost"])
        # assert flag, "数据比较不一致"

