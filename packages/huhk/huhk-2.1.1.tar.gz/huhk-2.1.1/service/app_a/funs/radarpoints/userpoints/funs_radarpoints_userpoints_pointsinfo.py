import allure

from service.app_a.asserts.radarpoints.userpoints.asserts_radarpoints_userpoints_pointsinfo import AssertsRadarpointsUserpointsPointsinfo
from service.app_a.apis.radarpoints.userpoints import apis_radarpoints_userpoints_pointsinfo


class FunsRadarpointsUserpointsPointsinfo(AssertsRadarpointsUserpointsPointsinfo):
    @allure.step(title="用户中心-积分明细-分页查询")
    def radarpoints_userpoints_pointsinfo_pagelist(self, userId="$None$", current=1, changeTimeBegin="$None$", changeTimeEnd="$None$", name="$None$", size=10, businessSceneType="$None$", _assert=True,  **kwargs):
        """
            url=/radarpoints/userPoints/pointsInfo/pageList
                params: size :  : 每页大小
                params: current :  : 当前页
                params: businessSceneType :  : 10001 转介裂变
                10002 营销活动
                10003 社区活跃
                10004 线下活动
                10005 用车行为
                10006 评价
                10007 内容奖励
                10008 后台管理手动操作
                20000 其他
                params: name :  : 名称
                params: changeTimeBegin :  : 变动开始时间
                params: changeTimeEnd :  : 变动结束时间
                params: headers : 请求头
        """
        userId = self.get_list_choice(userId, list_or_dict=None, key="userId")
        changeTimeBegin = self.get_list_choice(changeTimeBegin, list_or_dict=None, key="changeTimeBegin")
        changeTimeEnd = self.get_list_choice(changeTimeEnd, list_or_dict=None, key="changeTimeEnd")
        name = self.get_list_choice(name, list_or_dict=None, key="name")
        businessSceneType = self.get_list_choice(businessSceneType, list_or_dict=None, key="businessSceneType")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_radarpoints_userpoints_pointsinfo.radarpoints_userpoints_pointsinfo_pagelist(**_kwargs)

        self.assert_radarpoints_userpoints_pointsinfo_pagelist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


