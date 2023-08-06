import allure

from service.app_a import unit_request
from service.app_a.sqls.goods.sqls_goods_ordermain import SqlsGoodsOrdermain


class AssertsGoodsOrdermain(SqlsGoodsOrdermain):
    @allure.step(title="接口返回结果校验")
    def assert_goods_ordermain_pay(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_goods_ordermain_pay(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["orderMainId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_goods_ordermain_orderexports(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_goods_ordermain_orderexports(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["endTime", "userMobile", "testDriveIdStr", "billStatus", "exportType", "shopName", "startTime", "modelName", "userName"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_goods_ordermain_getordermainpage(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_goods_ordermain_getordermainpage(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["shopName", "userMobile", "startTime", "endTime", "modelName", "orderStatus", "userName"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_goods_ordermain_getordermainbyid(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_goods_ordermain_getordermainbyid(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["orderMainId"])
        # assert flag, "数据比较不一致"

