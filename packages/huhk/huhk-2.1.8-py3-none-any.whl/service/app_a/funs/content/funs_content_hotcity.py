import allure

from service.app_a.asserts.content.asserts_content_hotcity import AssertsContentHotcity
from service.app_a.apis.content import apis_content_hotcity


class FunsContentHotcity(AssertsContentHotcity):
    @allure.step(title="热门城市-Y")
    def content_hotcity_list(self, _assert=True,  **kwargs):
        """
            url=/content/hotcity/list
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_hotcity.content_hotcity_list(**_kwargs)

        self.assert_content_hotcity_list(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


