import allure

from service.app_a.asserts.asserts_activitymanager import AssertsActivitymanager
from service.app_a.apis import apis_activitymanager


class FunsActivitymanager(AssertsActivitymanager):
    @allure.step(title="后台管理-置顶接口-Y")
    def activitymanager_updateactivitytop(self, activityId="$None$", topFlag="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/activityManager/updateActivityTop
                params: activityId : string : 活动主键
                params: topFlag : integer : 活动置顶标识 0-不置顶 1-置顶
                params: headers : 请求头
        """
        activityId = self.get_value_choice(activityId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        topFlag = self.get_value_choice(topFlag, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_activitymanager.activitymanager_updateactivitytop(**_kwargs)

        self.assert_activitymanager_updateactivitytop(_assert, **_kwargs)
        self.set_value(_kwargs)


