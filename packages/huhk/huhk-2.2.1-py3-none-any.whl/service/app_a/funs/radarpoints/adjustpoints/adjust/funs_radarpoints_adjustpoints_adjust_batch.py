import allure

from service.app_a.asserts.radarpoints.adjustpoints.adjust.asserts_radarpoints_adjustpoints_adjust_batch import AssertsRadarpointsAdjustpointsAdjustBatch
from service.app_a.apis.radarpoints.adjustpoints.adjust import apis_radarpoints_adjustpoints_adjust_batch


class FunsRadarpointsAdjustpointsAdjustBatch(AssertsRadarpointsAdjustpointsAdjustBatch):
    @allure.step(title="积分调整 - 批量调整")
    def radarpoints_adjustpoints_adjust_batch_save(self, redisKey="$None$", clientNotes="$None$", optAbilityName="$None$", adjustNotes="$None$", file="$None$", optAbility="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/radarpoints/adjustPoints/adjust/batch/save
                params: file : file : 导入excel文件
                params: optAbility : text : 调整方式
                params: adjustNotes : text : 调整原因说明
                params: clientNotes : text : 用户端展示
                params: optAbilityName : string : 调整方式枚举
                params: redisKey : string : 缓存键
                params: headers : 请求头
        """
        redisKey = self.get_value_choice(redisKey, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        clientNotes = self.get_value_choice(clientNotes, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        optAbilityName = self.get_value_choice(optAbilityName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        adjustNotes = self.get_value_choice(adjustNotes, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        file = self.get_value_choice(file, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        optAbility = self.get_value_choice(optAbility, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_radarpoints_adjustpoints_adjust_batch.radarpoints_adjustpoints_adjust_batch_save(**_kwargs)

        self.assert_radarpoints_adjustpoints_adjust_batch_save(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="积分调整 - 批量调整 - 导入excel")
    def radarpoints_adjustpoints_adjust_batch_import(self, list="$None$", field_34="$None$", clientNotes="$None$", adjustNotes="$None$", field_35="$None$", file="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/radarpoints/adjustPoints/adjust/batch/import
                params: file : file : excel文件
                params: adjustNotes : string : 调整原因说明
                params: clientNotes : string : 客户端显示信息
                params: list : array : 成功数据集
                userId : number : 用户id
                adjustTypeName : number : 调整类型名称
                adjustNumber : number : 调整数值
                pointsDepartment : number : 积分归属部门
                DateType : number : 生效时间类型
                params: field_35 : string :
                params: field_34 : string :
                params: headers : 请求头
        """
        list = self.get_value_choice(list, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        field_34 = self.get_value_choice(field_34, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        clientNotes = self.get_value_choice(clientNotes, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        adjustNotes = self.get_value_choice(adjustNotes, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        field_35 = self.get_value_choice(field_35, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        file = self.get_value_choice(file, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_radarpoints_adjustpoints_adjust_batch.radarpoints_adjustpoints_adjust_batch_import(**_kwargs)

        self.assert_radarpoints_adjustpoints_adjust_batch_import(_assert, **_kwargs)
        self.set_value(_kwargs)


