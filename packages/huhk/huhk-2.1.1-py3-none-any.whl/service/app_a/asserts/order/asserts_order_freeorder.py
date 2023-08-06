import allure

from service.app_a import unit_request
from service.app_a.sqls.order.sqls_order_freeorder import SqlsOrderFreeorder


class AssertsOrderFreeorder(SqlsOrderFreeorder):
    @allure.step(title="接口返回结果校验")
    def assert_order_freeorder_download(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_order_freeorder_download(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["provinceName", "freeOrderId", "provinceId", "regisTimeBegin", "avatarUrl", "createTime", "nickName", "modelId", "userPolicyCode", "channel", "privacyPolicyCode", "mobile", "cityName", "channelName", "regisTimeEnd", "cityId", "userName"])
        # assert flag, "数据比较不一致"

