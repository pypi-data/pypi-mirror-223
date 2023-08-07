import allure

from service.app_a import unit_request
from service.app_a.sqls.radarpoints.userpoints.sqls_radarpoints_userpoints_exchangeinfo import SqlsRadarpointsUserpointsExchangeinfo


class AssertsRadarpointsUserpointsExchangeinfo(SqlsRadarpointsUserpointsExchangeinfo):
    @allure.step(title="接口返回结果校验")
    def assert_radarpoints_userpoints_exchangeinfo_pagelist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_radarpoints_userpoints_exchangeinfo_pagelist(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId", "orderEndTime", "consigneeName", "goodsOrderId", "orderStartTime", "mobile"])
        # assert flag, "数据比较不一致"

