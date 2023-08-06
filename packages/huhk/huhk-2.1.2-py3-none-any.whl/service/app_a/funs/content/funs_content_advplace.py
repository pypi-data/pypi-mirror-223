import allure

from service.app_a.asserts.content.asserts_content_advplace import AssertsContentAdvplace
from service.app_a.apis.content import apis_content_advplace


class FunsContentAdvplace(AssertsContentAdvplace):
    @allure.step(title="点位-更新大点位内容")
    def content_advplace_updatename(self, advPlaceName="$None$", advPlaceId="$None$", playTime="$None$", startFlag="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/advplace/updateName
                params: advPlaceId : text :
                params: advPlaceName : text :
                params: startFlag : text : 广告页广告位必传
                params: playTime : text : 广告页广告位必传
                params: headers : 请求头
        """
        advPlaceName = self.get_value_choice(advPlaceName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        advPlaceId = self.get_value_choice(advPlaceId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        playTime = self.get_value_choice(playTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        startFlag = self.get_value_choice(startFlag, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_advplace.content_advplace_updatename(**_kwargs)

        self.assert_content_advplace_updatename(_assert, **_kwargs)
        self.set_value(_kwargs)


