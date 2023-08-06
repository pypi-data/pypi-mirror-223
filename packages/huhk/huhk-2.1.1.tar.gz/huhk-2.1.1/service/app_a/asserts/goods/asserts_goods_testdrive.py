import allure

from service.app_a import unit_request
from service.app_a.sqls.goods.sqls_goods_testdrive import SqlsGoodsTestdrive


class AssertsGoodsTestdrive(SqlsGoodsTestdrive):
    @allure.step(title="接口返回结果校验")
    def assert_goods_testdrive_driveexports(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_goods_testdrive_driveexports(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["shopName", "testDriveIdStr", "channel", "exportType", "mobile", "startTime", "endTime", "userName"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_goods_testdrive_page(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_goods_testdrive_page(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["shopName", "channel", "pageNum", "mobile", "startTime", "endTime", "userName"])
        # assert flag, "数据比较不一致"

