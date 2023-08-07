import allure

from service.app_a import unit_request
from service.app_a.sqls.radarpoints.adjustpoints.adjust.sqls_radarpoints_adjustpoints_adjust_single import SqlsRadarpointsAdjustpointsAdjustSingle


class AssertsRadarpointsAdjustpointsAdjustSingle(SqlsRadarpointsAdjustpointsAdjustSingle):
    @allure.step(title="接口返回结果校验")
    def assert_radarpoints_adjustpoints_adjust_single_save(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_radarpoints_adjustpoints_adjust_single_save(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId", "clientNotes", "qty", "pointsExpiration", "adjustNotes", "optAbility"])
        # assert flag, "数据比较不一致"

