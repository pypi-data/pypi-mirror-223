import allure

from service.app_a.asserts.common.asserts_common_user import AssertsCommonUser
from service.app_a.apis.common import apis_common_user


class FunsCommonUser(AssertsCommonUser):
    @allure.step(title="获取管理后台用户的小号（马甲）-Y")
    def common_user_getuservestlist(self, _assert=True,  **kwargs):
        """
            url=/common/user/getUserVestList
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_common_user.common_user_getuservestlist(**_kwargs)

        self.assert_common_user_getuservestlist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


