import allure

from service.app_a import unit_request
from service.app_a.sqls.sqls_app_a import SqlsAppA


class AssertsAppA(SqlsAppA):
    @allure.step(title="接口返回结果校验")
    def assert_page(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_page(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["districtNameSort", "dealerName", "shopBusinessType", "provinceNameSort", "dealerCode", "province", "city", "district", "cityNameSort", "dealerAddress"])
        # assert flag, "数据比较不一致"

