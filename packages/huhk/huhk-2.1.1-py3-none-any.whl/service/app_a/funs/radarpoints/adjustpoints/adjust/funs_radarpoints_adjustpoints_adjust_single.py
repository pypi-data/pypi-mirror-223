import allure

from service.app_a.asserts.radarpoints.adjustpoints.adjust.asserts_radarpoints_adjustpoints_adjust_single import AssertsRadarpointsAdjustpointsAdjustSingle
from service.app_a.apis.radarpoints.adjustpoints.adjust import apis_radarpoints_adjustpoints_adjust_single


class FunsRadarpointsAdjustpointsAdjustSingle(AssertsRadarpointsAdjustpointsAdjustSingle):
    @allure.step(title="积分调整 - 单次调整")
    def radarpoints_adjustpoints_adjust_single_save(self, userId="$None$", clientNotes="$None$", qty="$None$", pointsExpiration="$None$", adjustNotes="$None$", optAbility="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/radarpoints/adjustPoints/adjust/single/save
                params: optAbility : number : 积分调整类型
                params: adjustNotes : string : 调整原因说明
                params: clientNotes : string : 户端展示信息
                params: qty : number : 调整数值
                params: pointsExpiration : number : 积分有效期类型（新增时赋值）
                params: headers : 请求头
        """
        userId = self.get_value_choice(userId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        clientNotes = self.get_value_choice(clientNotes, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        qty = self.get_value_choice(qty, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        pointsExpiration = self.get_value_choice(pointsExpiration, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        adjustNotes = self.get_value_choice(adjustNotes, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        optAbility = self.get_value_choice(optAbility, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_radarpoints_adjustpoints_adjust_single.radarpoints_adjustpoints_adjust_single_save(**_kwargs)

        self.assert_radarpoints_adjustpoints_adjust_single_save(_assert, **_kwargs)
        self.set_value(_kwargs)


