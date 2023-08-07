import allure

from service.app_a import unit_request
from service.app_a.sqls.goods.sqls_goods_carmodel import SqlsGoodsCarmodel


class AssertsGoodsCarmodel(SqlsGoodsCarmodel):
    @allure.step(title="接口返回结果校验")
    def assert_goods_carmodel_savemanagecarmodel(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_goods_carmodel_savemanagecarmodel(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["carDetailType", "preToDepositEndTime", "prePrice", "sharePosters", "price", "preEndTime", "carCode", "brandName", "modelName", "modelId", "modelCode", "carName", "depositStartTime", "depositPriceContent", "depositEndTime", "carSimpleName", "prePriceContent", "status", "promptDesc", "preToDepositStartTime", "preStartTime", "version", "carDetailPics", "carDetailUrl", "prePricePosters", "sort", "configCode", "depositPrice", "posters"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_goods_carmodel_removebyid(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_goods_carmodel_removebyid(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["modelId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_goods_carmodel_getcarmodelmanagebyid(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_goods_carmodel_getcarmodelmanagebyid(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["modelId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_goods_carmodel_getmanagecarmodel(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_goods_carmodel_getmanagecarmodel(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["modelCode", "carName", "operator", "version", "carCode", "brandName", "modelName", "status"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_goods_carmodel_getmodelnamelist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_goods_carmodel_getmodelnamelist(**kwargs)
        # flag = self.compare_json_list(self.res, out, [])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_goods_carmodel_getcarnamelist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_goods_carmodel_getcarnamelist(**kwargs)
        # flag = self.compare_json_list(self.res, out, [])
        # assert flag, "数据比较不一致"

