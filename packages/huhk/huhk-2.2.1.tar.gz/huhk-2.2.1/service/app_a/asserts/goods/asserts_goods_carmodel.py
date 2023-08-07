import allure

from service.app_a import unit_request
from service.app_a.sqls.goods.sqls_goods_carmodel import SqlsGoodsCarmodel


class AssertsGoodsCarmodel(SqlsGoodsCarmodel):
    @allure.step(title="接口返回结果校验")
    def assert_goods_carmodel_savemanagecarmodel(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_goods_carmodel_savemanagecarmodel(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["prePricePosters", "modelCode", "price", "status", "posters", "preEndTime", "modelName", "promptDesc", "prePrice", "carDetailPics", "preToDepositEndTime", "depositStartTime", "carSimpleName", "depositPrice", "sharePosters", "brandName", "preStartTime", "depositPriceContent", "version", "carName", "configCode", "depositEndTime", "prePriceContent", "preToDepositStartTime", "modelId", "carCode", "carDetailType", "carDetailUrl", "sort"])
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
        # flag = self.compare_json_list(self.res, out, ["carName", "modelCode", "brandName", "status", "carCode", "version", "operator", "modelName"])
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

