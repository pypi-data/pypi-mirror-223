import allure

from service.app_a.asserts.common.asserts_common_remoteinterfacelog import AssertsCommonRemoteinterfacelog
from service.app_a.apis.common import apis_common_remoteinterfacelog


class FunsCommonRemoteinterfacelog(AssertsCommonRemoteinterfacelog):
    @allure.step(title="查询三方日志接口-Y")
    def common_remoteinterfacelog_getlogpage(self, current=1, mobile="$None$", startTime="$None$", endTime="$None$", interfaceType="$None$", userName="$None$", size=10, _assert=True,  **kwargs):
        """
            url=/common/remoteinterfacelog/getLogPage
                params: interfaceType :  : 日志类型（1.支付日志  2.退款日志  3.换电日志）
                params: startTime :  : 开始时间
                params: endTime :  : 结束时间
                params: userName :  : 用户昵称
                params: mobile :  : 手机号
                params: size :  : 每页条数
                params: current :  : 当前页
                params: headers : 请求头
        """
        mobile = self.get_list_choice(mobile, list_or_dict=None, key="mobile")
        startTime = self.get_list_choice(startTime, list_or_dict=None, key="startTime")
        endTime = self.get_list_choice(endTime, list_or_dict=None, key="endTime")
        interfaceType = self.get_list_choice(interfaceType, list_or_dict=None, key="interfaceType")
        userName = self.get_list_choice(userName, list_or_dict=None, key="userName")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_common_remoteinterfacelog.common_remoteinterfacelog_getlogpage(**_kwargs)

        self.assert_common_remoteinterfacelog_getlogpage(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


