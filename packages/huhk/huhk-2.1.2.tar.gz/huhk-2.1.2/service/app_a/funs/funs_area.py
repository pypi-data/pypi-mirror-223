import allure

from service.app_a.asserts.asserts_area import AssertsArea
from service.app_a.apis import apis_area


class FunsArea(AssertsArea):
    @allure.step(title="限行城市-D")
    def area_getcitylist(self, _assert=True,  **kwargs):
        """
            url=/area/getCityList
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_area.area_getcitylist(**_kwargs)

        self.assert_area_getcitylist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


