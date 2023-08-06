import allure

from service.app_a.asserts.radarpoints.asserts_radarpoints_pointsconfig import AssertsRadarpointsPointsconfig
from service.app_a.apis.radarpoints import apis_radarpoints_pointsconfig


class FunsRadarpointsPointsconfig(AssertsRadarpointsPointsconfig):
    @allure.step(title="积分配置 - 分页查询")
    def radarpoints_pointsconfig_page(self, pointsBegin="$None$", Current="$None$", status="$None$", name="$None$", pointsEnd="$None$", pointsExpiration="$None$", size=10, code="$None$", businessSceneType="$None$", _assert=True,  **kwargs):
        """
            url=/radarpoints/PointsConfig/page
                params: code :  : 积分项Code
                params: name :  : 积分项名称
                params: businessSceneType :  : 发放场景类型
                params: pointsBegin :  : 积分值 - 开始区间
                params: pointsEnd :  : 积分值 - 结束区间
                params: pointsExpiration :  : 积分有效期
                params: status :  : 生效状态（0未生效，1已生效）
                params: Current :  : 当前页
                params: size :  : 每页大小
                params: headers : 请求头
        """
        pointsBegin = self.get_list_choice(pointsBegin, list_or_dict=None, key="pointsBegin")
        Current = self.get_list_choice(Current, list_or_dict=None, key="Current")
        status = self.get_list_choice(status, list_or_dict=None, key="status")
        name = self.get_list_choice(name, list_or_dict=None, key="name")
        pointsEnd = self.get_list_choice(pointsEnd, list_or_dict=None, key="pointsEnd")
        pointsExpiration = self.get_list_choice(pointsExpiration, list_or_dict=None, key="pointsExpiration")
        code = self.get_list_choice(code, list_or_dict=None, key="code")
        businessSceneType = self.get_list_choice(businessSceneType, list_or_dict=None, key="businessSceneType")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_radarpoints_pointsconfig.radarpoints_pointsconfig_page(**_kwargs)

        self.assert_radarpoints_pointsconfig_page(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="积分配置 -新增积分配置")
    def radarpoints_pointsconfig_insert(self, remark="$None$", rulesPointsDayMax="$None$", businessSceneType="$None$", pointsExpiration="$None$", userPointsDayMax="$None$", toast="$None$", bpmId="$None$", points="$None$", name="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/radarpoints/PointsConfig/insert
                params: pointsExpiration : string : 积分有效期
                params: remark : string : 备注
                params: points : integer : 积分值
                params: toast : string : toast内容
                params: name : string : 积分项名称
                params: businessSceneType : integer : 发放场景类型
                params: bpmId : integer : bpm单号
                params: userPointsDayMax : integer : 单用户单日上限
                params: rulesPointsDayMax : integer : 单日上限
                params: headers : 请求头
        """
        remark = self.get_value_choice(remark, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        rulesPointsDayMax = self.get_value_choice(rulesPointsDayMax, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        businessSceneType = self.get_value_choice(businessSceneType, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        pointsExpiration = self.get_value_choice(pointsExpiration, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        userPointsDayMax = self.get_value_choice(userPointsDayMax, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        toast = self.get_value_choice(toast, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        bpmId = self.get_value_choice(bpmId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        points = self.get_value_choice(points, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        name = self.get_value_choice(name, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_radarpoints_pointsconfig.radarpoints_pointsconfig_insert(**_kwargs)

        self.assert_radarpoints_pointsconfig_insert(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="积分配置 -修改积分配置")
    def radarpoints_pointsconfig_update(self, remark="$None$", id="$None$", rulesPointsDayMax="$None$", businessSceneType="$None$", pointsExpiration="$None$", code="$None$", userPointsDayMax="$None$", toast="$None$", bpmId="$None$", points="$None$", name="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/radarpoints/PointsConfig/update
                params: pointsExpiration : string : 积分有效期
                params: remark : string : 备注
                params: points : integer : 积分值
                params: toast : string : toast内容
                params: name : string : 积分项名称
                params: businessSceneType : integer : 发放场景类型
                params: id : integer : 积分项id
                params: code : string : 积分项code
                params: rulesPointsDayMax : integer : 单日上限
                params: userPointsDayMax : integer : 单用户单日上限
                params: bpmId : integer : bpm单号
                params: headers : 请求头
        """
        remark = self.get_value_choice(remark, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        id = self.get_value_choice(id, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        rulesPointsDayMax = self.get_value_choice(rulesPointsDayMax, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        businessSceneType = self.get_value_choice(businessSceneType, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        pointsExpiration = self.get_value_choice(pointsExpiration, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        code = self.get_value_choice(code, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        userPointsDayMax = self.get_value_choice(userPointsDayMax, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        toast = self.get_value_choice(toast, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        bpmId = self.get_value_choice(bpmId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        points = self.get_value_choice(points, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        name = self.get_value_choice(name, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_radarpoints_pointsconfig.radarpoints_pointsconfig_update(**_kwargs)

        self.assert_radarpoints_pointsconfig_update(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="积分配置 -生效状态变更")
    def radarpoints_pointsconfig_updatestatusbyid(self, id="$None$", status="$None$", _assert=True,  **kwargs):
        """
            url=/radarpoints/PointsConfig/updateStatusById
                params: id :  : 积分id
                params: status :  : 生效状态（0未生效，1已生效）
                params: headers : 请求头
        """
        id = self.get_list_choice(id, list_or_dict=None, key="id")
        status = self.get_list_choice(status, list_or_dict=None, key="status")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_radarpoints_pointsconfig.radarpoints_pointsconfig_updatestatusbyid(**_kwargs)

        self.assert_radarpoints_pointsconfig_updatestatusbyid(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


