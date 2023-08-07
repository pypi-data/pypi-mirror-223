import allure

from service.app_a.asserts.admin.asserts_admin_spa import AssertsAdminSpa
from service.app_a.apis.admin import apis_admin_spa


class FunsAdminSpa(AssertsAdminSpa):
    @allure.step(title="获取guc appId")
    def admin_spa_getappid(self, _assert=True,  **kwargs):
        """
            url=/admin/spa/getAppId
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_admin_spa.admin_spa_getappid(**_kwargs)

        self.assert_admin_spa_getappid(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


