import allure

from service.app_a import unit_request
from service.app_a.sqls.content.sqls_content_agreement import SqlsContentAgreement


class AssertsContentAgreement(SqlsContentAgreement):
    @allure.step(title="接口返回结果校验")
    def assert_content_agreement_getagreement(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_agreement_getagreement(**kwargs)
        # flag = self.compare_json_list(self.res, out, [])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_agreement_getbycode(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_agreement_getbycode(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["agreementCode"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_agreement_getagreementbycode(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_agreement_getagreementbycode(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["agreementCode"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_agreement_updatestatus(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_agreement_updatestatus(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["code", "agreementId", "status"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_agreement_list(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_agreement_list(**kwargs)
        # flag = self.compare_json_list(self.res, out, [])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_agreement_save(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_agreement_save(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["code", "content", "name", "version"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_agreement_update(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_agreement_update(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["code", "name", "agreementId", "version", "content"])
        # assert flag, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_content_agreement_getbyid(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_content_agreement_getbyid(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["agreementId"])
        # assert flag, "数据比较不一致"

