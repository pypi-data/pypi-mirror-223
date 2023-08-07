import allure

from service.app_a import unit_request
from service.app_a.sqls.content.sqls_content_campmanager import SqlsContentCampmanager


class AssertsContentCampmanager(SqlsContentCampmanager):
    @allure.step(title="接口返回结果校验")
    def assert_content_campmanager_page(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_campmanager_page(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["createBy", "id", "status", "sortBody", "sortord", "name"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_campmanager_soldout(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_campmanager_soldout(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["campId", "id"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_campmanager_insertcampid(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_campmanager_insertcampid(**kwargs)
        # flag = self.compare_json_list(self.res, out, [])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_campmanager_insert(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_campmanager_insert(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["content", "id", "county", "url", "province", "city", "campTradeTime", "campDetail", "address", "ownerDiscount", "discountExpEndTime", "discountExpBeginTime", "name"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_campmanager_detail_(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_campmanager_detail_(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["id"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_campmanager_update(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_campmanager_update(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["phone", "areaCode", "ownerDiscount", "discountExpEndTime", "discountExpBeginTime"])
        # assert flag, "数据比较不一致"

