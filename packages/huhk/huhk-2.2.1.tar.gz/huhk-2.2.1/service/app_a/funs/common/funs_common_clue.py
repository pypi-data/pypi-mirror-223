import allure

from service.app_a.asserts.common.asserts_common_clue import AssertsCommonClue
from service.app_a.apis.common import apis_common_clue


class FunsCommonClue(AssertsCommonClue):
    @allure.step(title="用户列表-详情-查询线索-Y")
    def common_clue_getclueuserpage(self, current=1, userId="$None$", size=10, _assert=True,  **kwargs):
        """
            url=/common/clue/getClueUserPage
                params: current :  : 页码
                params: size :  : 每页大小
                params: headers : 请求头
        """
        userId = self.get_list_choice(userId, list_or_dict=None, key="userId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_common_clue.common_clue_getclueuserpage(**_kwargs)

        self.assert_common_clue_getclueuserpage(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


