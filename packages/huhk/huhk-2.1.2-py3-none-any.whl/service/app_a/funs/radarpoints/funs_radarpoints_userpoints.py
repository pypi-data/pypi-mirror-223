from service.app_a.apis.radarpoints import apis_radarpoints_userpoints
from service.app_a.asserts.radarpoints.asserts_radarpoints_userpoints import AssertsRadarpointsUserpoints
import allure
from service.app_a.funs.radarpoints.userpoints.funs_radarpoints_userpoints_pointsinfo import FunsRadarpointsUserpointsPointsinfo
from service.app_a.funs.radarpoints.userpoints.funs_radarpoints_userpoints_exchangeinfo import FunsRadarpointsUserpointsExchangeinfo


class FunsRadarpointsUserpoints(FunsRadarpointsUserpointsPointsinfo, FunsRadarpointsUserpointsExchangeinfo, AssertsRadarpointsUserpoints):
    @allure.step(title="用户积分 - 分页查询")
    def radarpoints_userpoints_pagelist(self, cumulativeAcquisitionMost="$None$", userId="$None$", registrationTimeBegin="$None$", physicalIntegralLeast="$None$", nickName="$None$", cumulativeAcquisitionLeast="$None$", freezeQtyLeast="$None$", current=1, conversionFrequencyLeast="$None$", registrationTimeEnd="$None$", mobile="$None$", physicalIntegralMost="$None$", cumulativeConsumptionLeast="$None$", conversionFrequencyMost="$None$", freezeQtyMost="$None$", size=10, cumulativeConsumptionMost="$None$", _assert=True,  **kwargs):
        """
            url=/radarpoints/userPoints/pageList
                params: mobile :  : 用户手机号
                params: nickName :  : 用户昵称
                params: registrationTimeBegin :  : 注册时间 - 开始
                params: registrationTimeEnd :  : 注册时间 - 结束
                params: physicalIntegralLeast :  : 持有积分 - 最少
                params: physicalIntegralMost :  : 持有积分 - 最多
                params: cumulativeAcquisitionLeast :  : 累计获取 - 最少
                params: cumulativeAcquisitionMost :  : 累计获取 - 最多
                params: cumulativeConsumptionLeast :  : 累计消耗 - 最少
                params: cumulativeConsumptionMost :  : 累计消耗 - 最多
                params: conversionFrequencyLeast :  : 兑换次数 - 最少
                params: conversionFrequencyMost :  : 兑换次数 - 最多
                params: freezeQtyLeast :  : 冻结积分 - 最少
                params: freezeQtyMost :  : 冻结积分 - 最多
                params: current :  : 页码
                params: size :  : 每页大小
                params: headers : 请求头
        """
        cumulativeAcquisitionMost = self.get_list_choice(cumulativeAcquisitionMost, list_or_dict=None, key="cumulativeAcquisitionMost")
        userId = self.get_list_choice(userId, list_or_dict=None, key="userId")
        registrationTimeBegin = self.get_list_choice(registrationTimeBegin, list_or_dict=None, key="registrationTimeBegin")
        physicalIntegralLeast = self.get_list_choice(physicalIntegralLeast, list_or_dict=None, key="physicalIntegralLeast")
        nickName = self.get_list_choice(nickName, list_or_dict=None, key="nickName")
        cumulativeAcquisitionLeast = self.get_list_choice(cumulativeAcquisitionLeast, list_or_dict=None, key="cumulativeAcquisitionLeast")
        freezeQtyLeast = self.get_list_choice(freezeQtyLeast, list_or_dict=None, key="freezeQtyLeast")
        conversionFrequencyLeast = self.get_list_choice(conversionFrequencyLeast, list_or_dict=None, key="conversionFrequencyLeast")
        registrationTimeEnd = self.get_list_choice(registrationTimeEnd, list_or_dict=None, key="registrationTimeEnd")
        mobile = self.get_list_choice(mobile, list_or_dict=None, key="mobile")
        physicalIntegralMost = self.get_list_choice(physicalIntegralMost, list_or_dict=None, key="physicalIntegralMost")
        cumulativeConsumptionLeast = self.get_list_choice(cumulativeConsumptionLeast, list_or_dict=None, key="cumulativeConsumptionLeast")
        conversionFrequencyMost = self.get_list_choice(conversionFrequencyMost, list_or_dict=None, key="conversionFrequencyMost")
        freezeQtyMost = self.get_list_choice(freezeQtyMost, list_or_dict=None, key="freezeQtyMost")
        cumulativeConsumptionMost = self.get_list_choice(cumulativeConsumptionMost, list_or_dict=None, key="cumulativeConsumptionMost")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_radarpoints_userpoints.radarpoints_userpoints_pagelist(**_kwargs)

        self.assert_radarpoints_userpoints_pagelist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="用户积分 - 导出excel")
    def radarpoints_userpoints_export(self, cumulativeAcquisitionMost="$None$", registrationTimeBegin="$None$", physicalIntegralLeast="$None$", pageSize="$None$", nickName="$None$", cumulativeAcquisitionLeast="$None$", conversionFrequencyLeast="$None$", registrationTimeEnd="$None$", currentPage="$None$", physicalIntegralMost="$None$", cumulativeConsumptionLeast="$None$", conversionFrequencyMost="$None$", cumulativeConsumptionMost="$None$", _assert=True,  **kwargs):
        """
            url=/radarpoints/userPoints/export
                params: nickName :  : 用户昵称
                params: registrationTimeBegin :  : 注册时间 - 开始
                params: registrationTimeEnd :  : 注册时间 - 结束
                params: physicalIntegralLeast :  : 持有积分 - 最少
                params: physicalIntegralMost :  : 持有积分 - 最多
                params: cumulativeAcquisitionLeast :  : 累计获取 - 最少
                params: cumulativeAcquisitionMost :  : 累计获取 - 最多
                params: cumulativeConsumptionLeast :  : 累计消耗 - 最少
                params: cumulativeConsumptionMost :  : 累计消耗 - 最多
                params: conversionFrequencyLeast :  : 兑换次数 - 最少
                params: conversionFrequencyMost :  : 兑换次数 - 最多
                params: currentPage :  : 当前页码
                params: pageSize :  : 每页大小
                params: headers : 请求头
        """
        cumulativeAcquisitionMost = self.get_list_choice(cumulativeAcquisitionMost, list_or_dict=None, key="cumulativeAcquisitionMost")
        registrationTimeBegin = self.get_list_choice(registrationTimeBegin, list_or_dict=None, key="registrationTimeBegin")
        physicalIntegralLeast = self.get_list_choice(physicalIntegralLeast, list_or_dict=None, key="physicalIntegralLeast")
        pageSize = self.get_list_choice(pageSize, list_or_dict=None, key="pageSize")
        nickName = self.get_list_choice(nickName, list_or_dict=None, key="nickName")
        cumulativeAcquisitionLeast = self.get_list_choice(cumulativeAcquisitionLeast, list_or_dict=None, key="cumulativeAcquisitionLeast")
        conversionFrequencyLeast = self.get_list_choice(conversionFrequencyLeast, list_or_dict=None, key="conversionFrequencyLeast")
        registrationTimeEnd = self.get_list_choice(registrationTimeEnd, list_or_dict=None, key="registrationTimeEnd")
        currentPage = self.get_list_choice(currentPage, list_or_dict=None, key="currentPage")
        physicalIntegralMost = self.get_list_choice(physicalIntegralMost, list_or_dict=None, key="physicalIntegralMost")
        cumulativeConsumptionLeast = self.get_list_choice(cumulativeConsumptionLeast, list_or_dict=None, key="cumulativeConsumptionLeast")
        conversionFrequencyMost = self.get_list_choice(conversionFrequencyMost, list_or_dict=None, key="conversionFrequencyMost")
        cumulativeConsumptionMost = self.get_list_choice(cumulativeConsumptionMost, list_or_dict=None, key="cumulativeConsumptionMost")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_radarpoints_userpoints.radarpoints_userpoints_export(**_kwargs)

        self.assert_radarpoints_userpoints_export(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


