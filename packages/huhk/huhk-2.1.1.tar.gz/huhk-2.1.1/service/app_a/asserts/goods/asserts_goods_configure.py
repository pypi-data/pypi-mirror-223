import allure

from service.app_a import unit_request
from service.app_a.sqls.goods.sqls_goods_configure import SqlsGoodsConfigure


class AssertsGoodsConfigure(SqlsGoodsConfigure):
    @allure.step(title="接口返回结果校验")
    def assert_goods_configure_savecarconfigure(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_goods_configure_savecarconfigure(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["salesVersionList", "optionalList", "appearanceColorList", "interiorColorList", "processColorList"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_goods_configure_getcarconfigurename(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_goods_configure_getcarconfigurename(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["modelId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_goods_configure_removecarconfigure(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_goods_configure_removecarconfigure(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["configureId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_goods_configure_updatecarconfigurestatus(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_goods_configure_updatecarconfigurestatus(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["configureId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_goods_configure_info(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_goods_configure_info(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["modelId"])
        # assert flag, "数据比较不一致"

