import allure

from service.app_a.asserts.admin.asserts_admin_guc import AssertsAdminGuc
from service.app_a.apis.admin import apis_admin_guc


class FunsAdminGuc(AssertsAdminGuc):
    @allure.step(title="guc登出")
    def admin_guc_guclogout(self, _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/admin/guc/gucLogout
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_admin_guc.admin_guc_guclogout(**_kwargs)

        self.assert_admin_guc_guclogout(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="guc登录回调")
    def admin_guc_guclogin(self, _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/admin/guc/gucLogin
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_admin_guc.admin_guc_guclogin(**_kwargs)

        self.assert_admin_guc_guclogin(_assert, **_kwargs)
        self.set_value(_kwargs)


