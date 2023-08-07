import allure

from service.app_a import unit_request
from service.app_a.sqls.content.sqls_content_material import SqlsContentMaterial


class AssertsContentMaterial(SqlsContentMaterial):
    @allure.step(title="接口返回结果校验")
    def assert_content_material_delgroup(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_material_delgroup(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["groupId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_material_delmaterial(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_material_delmaterial(**kwargs)
        # flag = self.compare_json_list(self.res, out, [])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_material_updategroup(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_material_updategroup(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["groupName", "groupId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_material_getmateriallist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_material_getmateriallist(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["groupId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_material_addgroup(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_material_addgroup(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["groupName"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_material_addmaterial(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_material_addmaterial(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["file", "groupId"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_material_getgrouplist(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_material_getgrouplist(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["groupName"])
        # assert flag, "数据比较不一致"

