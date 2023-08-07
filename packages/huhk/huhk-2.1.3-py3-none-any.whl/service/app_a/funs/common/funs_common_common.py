import allure

from service.app_a.asserts.common.asserts_common_common import AssertsCommonCommon
from service.app_a.apis.common import apis_common_common


class FunsCommonCommon(AssertsCommonCommon):
    @allure.step(title="文章-获取发布渠道-Y")
    def common_common_getchannel(self, _assert=True,  **kwargs):
        """
            url=/common/common/getChannel
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_common_common.common_common_getchannel(**_kwargs)

        self.assert_common_common_getchannel(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


