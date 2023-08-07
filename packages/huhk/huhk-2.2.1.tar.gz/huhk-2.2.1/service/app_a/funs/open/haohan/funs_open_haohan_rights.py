import allure

from service.app_a.asserts.open.haohan.asserts_open_haohan_rights import AssertsOpenHaohanRights
from service.app_a.apis.open.haohan import apis_open_haohan_rights


class FunsOpenHaohanRights(AssertsOpenHaohanRights):
    @allure.step(title="浩瀚模块 - 更改充电桩权益状态-Y")
    def open_haohan_rights_update(self, params="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/open/haohan/rights/update
                params: params : object :
                data : string : 加密数据
                params: headers : 请求头
        """
        params = self.get_value_choice(params, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_open_haohan_rights.open_haohan_rights_update(**_kwargs)

        self.assert_open_haohan_rights_update(_assert, **_kwargs)
        self.set_value(_kwargs)


