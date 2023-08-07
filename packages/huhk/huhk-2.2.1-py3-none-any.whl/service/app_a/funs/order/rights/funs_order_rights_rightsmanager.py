import allure

from service.app_a.asserts.order.rights.asserts_order_rights_rightsmanager import AssertsOrderRightsRightsmanager
from service.app_a.apis.order.rights import apis_order_rights_rightsmanager


class FunsOrderRightsRightsmanager(AssertsOrderRightsRightsmanager):
    @allure.step(title="自动生成权益ID-Y")
    def order_rights_rightsmanager_createid(self, _assert=True,  **kwargs):
        """
            url=/order/rights/rightsManager/createId
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_rights_rightsmanager.order_rights_rightsmanager_createid(**_kwargs)

        self.assert_order_rights_rightsmanager_createid(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="查询互斥关系接口-Y")
    def order_rights_rightsmanager_getrelation(self, rightsId="$None$", _assert=True,  **kwargs):
        """
            url=/order/rights/rightsManager/getRelation
                params: rightsId :  :
                params: headers : 请求头
        """
        rightsId = self.get_list_choice(rightsId, list_or_dict=None, key="rightsId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_rights_rightsmanager.order_rights_rightsmanager_getrelation(**_kwargs)

        self.assert_order_rights_rightsmanager_getrelation(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="权益 - 分页查询-Y")
    def order_rights_rightsmanager_page(self, modelCode="$None$", current=1, effectiveEndDate="$None$", status="$None$", rightsName="$None$", size=10, _assert=True,  **kwargs):
        """
            url=/order/rights/rightsManager/page
                params: size :  :
                params: current :  :
                params: rightsName :  :
                params: status :  :
                params: modelCode :  :
                params: effectiveEndDate :  :
                params: headers : 请求头
        """
        modelCode = self.get_list_choice(modelCode, list_or_dict=None, key="modelCode")
        effectiveEndDate = self.get_list_choice(effectiveEndDate, list_or_dict=None, key="effectiveEndDate")
        status = self.get_list_choice(status, list_or_dict=None, key="status")
        rightsName = self.get_list_choice(rightsName, list_or_dict=None, key="rightsName")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_rights_rightsmanager.order_rights_rightsmanager_page(**_kwargs)

        self.assert_order_rights_rightsmanager_page(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="权益订单 - 查询-Y")
    def order_rights_rightsmanager_getrightslist(self, modelId="$None$", effectiveStartDate="$None$", status="$None$", rightsName="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/order/rights/rightsManager/getRightsList
                params: rightsName : string : 权益名称
                params: status : integer : 权益状态(0未生效，1已生效)
                params: modelId : string : 车型代码
                params: effectiveStartDate : string : 权益生效时间
                params: headers : 请求头
        """
        modelId = self.get_value_choice(modelId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        effectiveStartDate = self.get_value_choice(effectiveStartDate, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        status = self.get_value_choice(status, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        rightsName = self.get_value_choice(rightsName, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_rights_rightsmanager.order_rights_rightsmanager_getrightslist(**_kwargs)

        self.assert_order_rights_rightsmanager_getrightslist(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="权益-新增权益-Y")
    def order_rights_rightsmanager_insert(self, modelCode="$None$", effectiveStartDate="$None$", rightsId="$None$", orderType="$None$", rightsType="$None$", rightsName="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/order/rights/rightsManager/insert
                params: effectiveStartDate : text : 权益生效时间 -- 开始
                params: rightsId : text : 权益ID
                params: rightsName : text : 权益名称
                params: rightsType : text : 权益类型
                params: modelCode : text : 车型代码
                params: orderType : text : 关联订单类型code
                params: headers : 请求头
        """
        modelCode = self.get_value_choice(modelCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        effectiveStartDate = self.get_value_choice(effectiveStartDate, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        rightsId = self.get_value_choice(rightsId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        orderType = self.get_value_choice(orderType, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        rightsType = self.get_value_choice(rightsType, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        rightsName = self.get_value_choice(rightsName, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_rights_rightsmanager.order_rights_rightsmanager_insert(**_kwargs)

        self.assert_order_rights_rightsmanager_insert(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="权益-修改权益-Y")
    def order_rights_rightsmanager_update(self, effectiveStartDate="$None$", Content="$None$", rightsId="$None$", effectiveEndDate="$None$", rightsName="$None$", Relation="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/order/rights/rightsManager/update
                params: rightsName : string : 权益名称
                params: rightsId : string : 权益主键
                params: Content : string : 权益描述
                params: effectiveStartDate : string : 权益生效时间
                params: effectiveEndDate : string : 权益生效时间-结束
                params: Relation : string : 互斥关系
                params: headers : 请求头
        """
        effectiveStartDate = self.get_value_choice(effectiveStartDate, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        Content = self.get_value_choice(Content, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        rightsId = self.get_value_choice(rightsId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        effectiveEndDate = self.get_value_choice(effectiveEndDate, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        rightsName = self.get_value_choice(rightsName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        Relation = self.get_value_choice(Relation, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_rights_rightsmanager.order_rights_rightsmanager_update(**_kwargs)

        self.assert_order_rights_rightsmanager_update(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="权益-获取权益详情-Y")
    def order_rights_rightsmanager_rightsbyid(self, id="$None$", _assert=True,  **kwargs):
        """
            url=/order/rights/rightsManager/rightsById
                params: id :  :
                params: headers : 请求头
        """
        id = self.get_list_choice(id, list_or_dict=None, key="id")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_rights_rightsmanager.order_rights_rightsmanager_rightsbyid(**_kwargs)

        self.assert_order_rights_rightsmanager_rightsbyid(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="权益-通过id更新权益生效状态-Y")
    def order_rights_rightsmanager_updatestatusbyid(self, rightsId="$None$", status="$None$", _assert=True,  **kwargs):
        """
            url=/order/rights/rightsManager/updateStatusById
                params: rightsId :  :
                params: status :  :
                params: headers : 请求头
        """
        rightsId = self.get_list_choice(rightsId, list_or_dict=None, key="rightsId")
        status = self.get_list_choice(status, list_or_dict=None, key="status")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_rights_rightsmanager.order_rights_rightsmanager_updatestatusbyid(**_kwargs)

        self.assert_order_rights_rightsmanager_updatestatusbyid(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


