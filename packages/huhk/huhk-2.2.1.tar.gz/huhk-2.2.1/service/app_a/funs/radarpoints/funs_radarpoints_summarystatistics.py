import allure

from service.app_a.asserts.radarpoints.asserts_radarpoints_summarystatistics import AssertsRadarpointsSummarystatistics
from service.app_a.apis.radarpoints import apis_radarpoints_summarystatistics


class FunsRadarpointsSummarystatistics(AssertsRadarpointsSummarystatistics):
    @allure.step(title="积分汇总统计-分页查询积分")
    def radarpoints_summarystatistics_pagelist(self, current=1, flowTimeBefore="$None$", size=10, flowTimeEnd="$None$", _assert=True,  **kwargs):
        """
            url=/radarpoints/summaryStatistics/pageList
                params: current :  :
                params: size :  :
                params: flowTimeBefore :  : 流水开始时间
                params: flowTimeEnd :  : 流水结束时间
                params: headers : 请求头
        """
        flowTimeBefore = self.get_list_choice(flowTimeBefore, list_or_dict=None, key="flowTimeBefore")
        flowTimeEnd = self.get_list_choice(flowTimeEnd, list_or_dict=None, key="flowTimeEnd")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_radarpoints_summarystatistics.radarpoints_summarystatistics_pagelist(**_kwargs)

        self.assert_radarpoints_summarystatistics_pagelist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="积分汇总统计 - 导出")
    def radarpoints_summarystatistics_export(self, current=1, flowTimebefore="$None$", size=10, flowTimeEnd="$None$", _assert=True,  **kwargs):
        """
            url=/radarpoints/summaryStatistics/export
                params: current :  :
                params: size :  :
                params: flowTimeEnd :  :
                params: flowTimebefore :  :
                params: headers : 请求头
        """
        flowTimebefore = self.get_list_choice(flowTimebefore, list_or_dict=None, key="flowTimebefore")
        flowTimeEnd = self.get_list_choice(flowTimeEnd, list_or_dict=None, key="flowTimeEnd")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_radarpoints_summarystatistics.radarpoints_summarystatistics_export(**_kwargs)

        self.assert_radarpoints_summarystatistics_export(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


