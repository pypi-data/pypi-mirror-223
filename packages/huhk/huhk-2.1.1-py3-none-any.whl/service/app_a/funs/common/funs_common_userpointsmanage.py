import allure

from service.app_a.asserts.common.asserts_common_userpointsmanage import AssertsCommonUserpointsmanage
from service.app_a.apis.common import apis_common_userpointsmanage


class FunsCommonUserpointsmanage(AssertsCommonUserpointsmanage):
    @allure.step(title="用户积分列表导出-历史接口")
    def common_userpointsmanage_userpointsexport(self, nickName="$None$", beginTime="$None$", mobile="$None$", logIds="$None$", endTime="$None$", _assert=True,  **kwargs):
        """
            url=/common/userPointsManage/userPointsExport
                params: nickName :  : 用户昵称
                params: mobile :  : 用户手机号
                params: beginTime :  : 注册时间查询范围--开始时间
                params: endTime :  : 注册时间查询范围--结束时间
                params: logIds :  : 积分明细Id，用于积分导出，如果传参表示勾选数据导出
                params: headers : 请求头
        """
        nickName = self.get_list_choice(nickName, list_or_dict=None, key="nickName")
        beginTime = self.get_list_choice(beginTime, list_or_dict=None, key="beginTime")
        mobile = self.get_list_choice(mobile, list_or_dict=None, key="mobile")
        logIds = self.get_list_choice(logIds, list_or_dict=None, key="logIds")
        endTime = self.get_list_choice(endTime, list_or_dict=None, key="endTime")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_common_userpointsmanage.common_userpointsmanage_userpointsexport(**_kwargs)

        self.assert_common_userpointsmanage_userpointsexport(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="用户积分列表查询-历史接口")
    def common_userpointsmanage_page(self, nickName="$None$", mobile="$None$", endTime="$None$", beginTime="$None$", _assert=True,  **kwargs):
        """
            url=/common/userPointsManage/page
                params: nickName :  :
                params: mobile :  :
                params: beginTime :  : 前端日期后面必须要追加 00:00:00
                params: endTime :  : 前端日期后面必须要追加 23:59:59
                params: headers : 请求头
        """
        nickName = self.get_list_choice(nickName, list_or_dict=None, key="nickName")
        mobile = self.get_list_choice(mobile, list_or_dict=None, key="mobile")
        endTime = self.get_list_choice(endTime, list_or_dict=None, key="endTime")
        beginTime = self.get_list_choice(beginTime, list_or_dict=None, key="beginTime")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_common_userpointsmanage.common_userpointsmanage_page(**_kwargs)

        self.assert_common_userpointsmanage_page(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="用户积分手动调整-历史接口")
    def common_userpointsmanage_manualchangeuserpoints(self, userId="$None$", operateMark="$None$", operatePoint="$None$", pointChangType="$None$", taskName="$None$", operateType="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/common/userPointsManage/manualChangeUserPoints
                params: operateType : string : 积分操作类型 目前只有 “增加” 一类
                params: operatePoint : integer : 操作的积分数量
                params: operateMark : string : 操作的积分备注
                params: taskName : string : 任务名称 注册 签到 消费
                params: pointChangType : number : 1--增加  2--消耗
                params: headers : 请求头
        """
        userId = self.get_value_choice(userId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        operateMark = self.get_value_choice(operateMark, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        operatePoint = self.get_value_choice(operatePoint, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        pointChangType = self.get_value_choice(pointChangType, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        taskName = self.get_value_choice(taskName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        operateType = self.get_value_choice(operateType, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_common_userpointsmanage.common_userpointsmanage_manualchangeuserpoints(**_kwargs)

        self.assert_common_userpointsmanage_manualchangeuserpoints(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="积分导出前置判断-历史接口")
    def common_userpointsmanage_beforepointsexport(self, nickName="$None$", beginTime="$None$", mobile="$None$", logIds="$None$", endTime="$None$", _assert=True,  **kwargs):
        """
            url=/common/userPointsManage/beforePointsExport
                params: nickName :  : 用户昵称
                params: mobile :  : 用户手机号
                params: beginTime :  : 注册时间查询范围--开始时间
                params: endTime :  : 注册时间查询范围--结束时间
                params: logIds :  : 积分明细Id，用于积分导出，如果传参表示勾选数据导出
                params: headers : 请求头
        """
        nickName = self.get_list_choice(nickName, list_or_dict=None, key="nickName")
        beginTime = self.get_list_choice(beginTime, list_or_dict=None, key="beginTime")
        mobile = self.get_list_choice(mobile, list_or_dict=None, key="mobile")
        logIds = self.get_list_choice(logIds, list_or_dict=None, key="logIds")
        endTime = self.get_list_choice(endTime, list_or_dict=None, key="endTime")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_common_userpointsmanage.common_userpointsmanage_beforepointsexport(**_kwargs)

        self.assert_common_userpointsmanage_beforepointsexport(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


