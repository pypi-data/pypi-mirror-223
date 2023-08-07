import allure

from service.app_a.asserts.radarpoints.asserts_radarpoints_pointstask import AssertsRadarpointsPointstask
from service.app_a.apis.radarpoints import apis_radarpoints_pointstask


class FunsRadarpointsPointstask(AssertsRadarpointsPointstask):
    @allure.step(title="积分任务 - 分页查询")
    def radarpoints_pointstask_pagelist(self, size=10, dateLast="$None$", getPointsQtySort="$None$", pointsConfigName="$None$", pointsTaskDateSort="$None$", mobile="$None$", pointsConfigCode="$None$", current=1, dateBegin="$None$", _assert=True,  **kwargs):
        """
            url=/radarpoints/pointsTask/pageList
                params: dateBegin :  : 开始日期
                params: dateLast :  : 结束日期
                params: pointsConfigCode :  : 任务编码
                params: pointsConfigName :  : 任务名称
                params: mobile :  : 用户手机号
                params: pointsTaskDateSort :  : 日期排序字段，"ASC"升序，"DESC"降序
                params: getPointsQtySort :  : 积分值排序字段，"ASC"升序，"DESC"降序
                params: current :  : 页码
                params: size :  : 每页大小
                params: headers : 请求头
        """
        dateLast = self.get_list_choice(dateLast, list_or_dict=None, key="dateLast")
        getPointsQtySort = self.get_list_choice(getPointsQtySort, list_or_dict=None, key="getPointsQtySort")
        pointsConfigName = self.get_list_choice(pointsConfigName, list_or_dict=None, key="pointsConfigName")
        pointsTaskDateSort = self.get_list_choice(pointsTaskDateSort, list_or_dict=None, key="pointsTaskDateSort")
        mobile = self.get_list_choice(mobile, list_or_dict=None, key="mobile")
        pointsConfigCode = self.get_list_choice(pointsConfigCode, list_or_dict=None, key="pointsConfigCode")
        dateBegin = self.get_list_choice(dateBegin, list_or_dict=None, key="dateBegin")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_radarpoints_pointstask.radarpoints_pointstask_pagelist(**_kwargs)

        self.assert_radarpoints_pointstask_pagelist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="积分任务 - 导出excel")
    def radarpoints_pointstask_export(self, dateLast="$None$", getPointsQtySort="$None$", pointsConfigName="$None$", pointsTaskDateSort="$None$", mobile="$None$", pointsConfigCode="$None$", dateBegin="$None$", _assert=True,  **kwargs):
        """
            url=/radarpoints/pointsTask/export
                params: dateBegin :  : 开始日期
                params: dateLast :  : 结束日期
                params: pointsConfigCode :  : 任务编码
                params: pointsConfigName :  : 任务名称
                params: mobile :  : 用户手机号
                params: pointsTaskDateSort :  : 日期排序字段，"ASC"升序，"DESC"降序
                params: getPointsQtySort :  : 积分值排序字段，"ASC"升序，"DESC"降序
                params: headers : 请求头
        """
        dateLast = self.get_list_choice(dateLast, list_or_dict=None, key="dateLast")
        getPointsQtySort = self.get_list_choice(getPointsQtySort, list_or_dict=None, key="getPointsQtySort")
        pointsConfigName = self.get_list_choice(pointsConfigName, list_or_dict=None, key="pointsConfigName")
        pointsTaskDateSort = self.get_list_choice(pointsTaskDateSort, list_or_dict=None, key="pointsTaskDateSort")
        mobile = self.get_list_choice(mobile, list_or_dict=None, key="mobile")
        pointsConfigCode = self.get_list_choice(pointsConfigCode, list_or_dict=None, key="pointsConfigCode")
        dateBegin = self.get_list_choice(dateBegin, list_or_dict=None, key="dateBegin")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_radarpoints_pointstask.radarpoints_pointstask_export(**_kwargs)

        self.assert_radarpoints_pointstask_export(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


