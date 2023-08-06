import allure

from service.app_a import unit_request
from service.app_a.sqls.manageapi.order.sqls_manageapi_order_mainorder import SqlsManageapiOrderMainorder


class AssertsManageapiOrderMainorder(SqlsManageapiOrderMainorder):
    @allure.step(title="接口返回结果校验")
    def assert_manageapi_order_mainorder_pagelist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_manageapi_order_mainorder_pagelist(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["provinceId", "orderStatus", "orderType", "extOrderStatus", "modelId", "createEndTime", "channel", "dealerCode", "createStartTime", "mobile", "cityId", "mainOrderId", "orderId", "extNum", "userName"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_manageapi_order_mainorder_detail(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_manageapi_order_mainorder_detail(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["orderId"])
        # assert flag, "数据比较不一致"

