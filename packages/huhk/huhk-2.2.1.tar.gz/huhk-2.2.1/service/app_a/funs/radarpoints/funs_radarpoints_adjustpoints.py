import allure

from service.app_a.asserts.radarpoints.asserts_radarpoints_adjustpoints import AssertsRadarpointsAdjustpoints
from service.app_a.apis.radarpoints import apis_radarpoints_adjustpoints
from service.app_a.funs.radarpoints.adjustpoints.funs_radarpoints_adjustpoints_adjust import FunsRadarpointsAdjustpointsAdjust


class FunsRadarpointsAdjustpoints(AssertsRadarpointsAdjustpoints, FunsRadarpointsAdjustpointsAdjust):
    @allure.step(title="积分调整 - 分页查询")
    def radarpoints_adjustpoints_pagelist(self, userId="$None$", nickName="$None$", current=1, optAbilityName="$None$", adjustTimeEnd="$None$", mobile="$None$", size=10, adjustNotes="$None$", optAbility="$None$", adjustTimeBefore="$None$", _assert=True,  **kwargs):
        """
            url=/radarpoints/adjustPoints/pageList
                params: nickName :  : 用户名
                params: mobile :  : 手机号
                params: adjustNotes :  : 调整原因说明
                params: optAbility :  : 调整积分方式
                params: optAbilityName :  : 调整积分方式枚举
                params: adjustTimeBefore :  : 调整时间 - 开始
                params: adjustTimeEnd :  : 调整时间 - 结束
                params: current :  : 页码
                params: size :  : 每页大小
                params: headers : 请求头
        """
        userId = self.get_list_choice(userId, list_or_dict=None, key="userId")
        nickName = self.get_list_choice(nickName, list_or_dict=None, key="nickName")
        optAbilityName = self.get_list_choice(optAbilityName, list_or_dict=None, key="optAbilityName")
        adjustTimeEnd = self.get_list_choice(adjustTimeEnd, list_or_dict=None, key="adjustTimeEnd")
        mobile = self.get_list_choice(mobile, list_or_dict=None, key="mobile")
        adjustNotes = self.get_list_choice(adjustNotes, list_or_dict=None, key="adjustNotes")
        optAbility = self.get_list_choice(optAbility, list_or_dict=None, key="optAbility")
        adjustTimeBefore = self.get_list_choice(adjustTimeBefore, list_or_dict=None, key="adjustTimeBefore")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_radarpoints_adjustpoints.radarpoints_adjustpoints_pagelist(**_kwargs)

        self.assert_radarpoints_adjustpoints_pagelist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="积分调整 - 根据UserId查询详情")
    def radarpoints_adjustpoints_getuserpointsqtybyuserid(self, userId="$None$", _assert=True,  **kwargs):
        """
            url=/radarpoints/adjustPoints/getUserPointsQtyByUserId
                params: headers : 请求头
        """
        userId = self.get_list_choice(userId, list_or_dict=None, key="userId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_radarpoints_adjustpoints.radarpoints_adjustpoints_getuserpointsqtybyuserid(**_kwargs)

        self.assert_radarpoints_adjustpoints_getuserpointsqtybyuserid(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="积分调整 - 根据Mobile查询详情")
    def radarpoints_adjustpoints_getuserpointsqtybymobile(self, mobile="$None$", _assert=True,  **kwargs):
        """
            url=/radarpoints/adjustPoints/getUserPointsQtyByMobile
                params: mobile :  : 手机号码
                params: headers : 请求头
        """
        mobile = self.get_list_choice(mobile, list_or_dict=None, key="mobile")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_radarpoints_adjustpoints.radarpoints_adjustpoints_getuserpointsqtybymobile(**_kwargs)

        self.assert_radarpoints_adjustpoints_getuserpointsqtybymobile(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="积分调整 - 导出excel")
    def radarpoints_adjustpoints_export(self, userId="$None$", nickName="$None$", current=1, optAbilityName="$None$", adjustTimeEnd="$None$", mobile="$None$", size=10, adjustNotes="$None$", optAbility="$None$", adjustTimeBefore="$None$", _assert=True,  **kwargs):
        """
            url=/radarpoints/adjustPoints/export
                params: nickName :  : 用户名
                params: mobile :  : 手机号
                params: adjustNotes :  : 调整原因说明
                params: optAbility :  : 调整积分方式
                params: optAbilityName :  : 调整积分方式枚举
                params: adjustTimeBefore :  : 调整时间 - 开始
                params: adjustTimeEnd :  : 调整时间 - 结束
                params: current :  : 页码
                params: size :  : 每页大小
                params: headers : 请求头
        """
        userId = self.get_list_choice(userId, list_or_dict=None, key="userId")
        nickName = self.get_list_choice(nickName, list_or_dict=None, key="nickName")
        optAbilityName = self.get_list_choice(optAbilityName, list_or_dict=None, key="optAbilityName")
        adjustTimeEnd = self.get_list_choice(adjustTimeEnd, list_or_dict=None, key="adjustTimeEnd")
        mobile = self.get_list_choice(mobile, list_or_dict=None, key="mobile")
        adjustNotes = self.get_list_choice(adjustNotes, list_or_dict=None, key="adjustNotes")
        optAbility = self.get_list_choice(optAbility, list_or_dict=None, key="optAbility")
        adjustTimeBefore = self.get_list_choice(adjustTimeBefore, list_or_dict=None, key="adjustTimeBefore")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_radarpoints_adjustpoints.radarpoints_adjustpoints_export(**_kwargs)

        self.assert_radarpoints_adjustpoints_export(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


