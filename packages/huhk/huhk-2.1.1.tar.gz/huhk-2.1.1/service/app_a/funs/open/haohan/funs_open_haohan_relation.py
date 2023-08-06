import allure

from service.app_a.asserts.open.haohan.asserts_open_haohan_relation import AssertsOpenHaohanRelation
from service.app_a.apis.open.haohan import apis_open_haohan_relation


class FunsOpenHaohanRelation(AssertsOpenHaohanRelation):
    @allure.step(title="浩瀚模块-关联关系-Y")
    def open_haohan_relation_update(self, userId="$None$", _assert=True,  **kwargs):
        """
            url=/open/haohan/relation/update
                params: headers : 请求头
        """
        userId = self.get_list_choice(userId, list_or_dict=None, key="userId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_open_haohan_relation.open_haohan_relation_update(**_kwargs)

        self.assert_open_haohan_relation_update(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


