import allure

from service.app_a.asserts.goods.asserts_goods_configure import AssertsGoodsConfigure
from service.app_a.apis.goods import apis_goods_configure


class FunsGoodsConfigure(AssertsGoodsConfigure):
    @allure.step(title="保存车型配置信息-Y")
    def goods_configure_savecarconfigure(self, salesVersionList="$None$", optionalList="$None$", appearanceColorList="$None$", interiorColorList="$None$", processColorList="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/goods/configure/saveCarConfigure
                params: salesVersionList : array : 销售版本
                configureId : string : 配置ID
                modelId : string : 关联的车型基础信息ID
                configureCode : string : 配置编码
                configureName : string : 配置名称
                saleVersion : string : 销售-版本号
                abbreviationList : array : 缩略图
                gwAbbreviationList : array : 官网缩略图
                defaultCarModelList : array : 默认车型
                gwDefaultCarModelList : array : 官网默认车型
                price : number : 零售价|加价
                sort : number : 前台权重
                versionDesc : string : 版本描述
                partsDesc : string : 配件描述
                status : number : 状态 （1:启用，0：禁用） 默认启用
                type : number : 1:销售版本,2:动力系统,3:外观颜色,4:内饰颜色,5:选装配置
                params: processColorList : array : 套色
                configureId : string : 配置ID
                modelId : string : 车型ID
                configureCode : string : 配置编码
                configureName : string : 配置名称
                saleVersionRelation : string : 关联销售版本 ALL代表全部多个版本以英文逗号隔开
                appearanceColorRelation : string : 套色、内饰关联的外观颜色，ALL代表全部多个版本以英文逗号隔开
                saleVersionContain : string : 价格已包含的版本， ALL代表全部多个版本以英文逗号隔开
                modificationName : string : 外观颜色|套色|内饰颜色|选装名称 - 修饰名称
                abbreviationList : array : 缩略图
                gwAbbreviationList : array : 官网缩略图
                defaultCarModelList : array : 默认车型
                gwDefaultCarModelList : array : 官网默认车型
                price : number : 加价
                sort : number : 排序
                versionDesc : string :
                partsDesc : string :
                status : number : 状态
                type : number : 类型
                params: appearanceColorList : array : 外观颜色
                configureId : string : 配置Id
                modelId : string : 车型ID
                configureCode : string : 配置编码
                configureName : string : 配置名称
                saleVersionRelation : string : 关联销售版本 ALL代表全部多个版本以英文逗号隔开
                appearanceColorRelation : string : 套色、内饰关联的外观颜色，ALL代表全部多个版本以英文逗号隔开
                saleVersionContain : string : 价格已包含的版本， ALL代表全部多个版本以英文逗号隔开
                modificationName : string : 外观颜色|套色|内饰颜色|选装名称 - 修饰名称
                abbreviationList : array : 缩略图
                gwAbbreviationList : array : 官网缩略图
                defaultCarModelList : array : 默认车型
                gwDefaultCarModelList : array : 官网默认车型
                price : number : 加价
                sort : number : 排序
                versionDesc : string :
                partsDesc : string :
                status : number : 状态
                type : number : 类型
                params: interiorColorList : array : 内饰颜色
                configureId : string : 配置ID
                modelId : string : 车型Id
                configureCode : string : 配置编码
                configureName : string : 配置名称
                saleVersionRelation : string : 关联销售版本 ALL代表全部多个版本以英文逗号隔开
                appearanceColorRelation : string : 套色、内饰关联的外观颜色，ALL代表全部多个版本以英文逗号隔开
                saleVersionContain : string : 价格已包含的版本， ALL代表全部多个版本以英文逗号隔开
                modificationName : string : 外观颜色|套色|内饰颜色|选装名称 - 修饰名称
                abbreviationList : array : 缩略图
                gwAbbreviationList : array : 官网缩略图
                defaultCarModelList : array : 默认车型
                gwDefaultCarModelList : array : 官网默认车型
                price : number : 加价
                sort : number : 排序
                versionDesc : string :
                partsDesc : string :
                status : number : 状态
                type : number : 类型
                params: optionalList : array : 选装配件
                configureId : string : 配置ID
                modelId : string : 车型ID
                configureCode : string : 配置编码
                configureName : string : 配置名称
                saleVersionRelation : string : 关联销售版本 ALL代表全部多个版本以英文逗号隔开
                appearanceColorRelation : string : 套色、内饰关联的外观颜色，ALL代表全部多个版本以英文逗号隔开
                saleVersionContain : string : 价格已包含的版本， ALL代表全部多个版本以英文逗号隔开
                modificationName : string : 外观颜色|套色|内饰颜色|选装名称 - 修饰名称
                abbreviationList : array : 缩略图
                gwAbbreviationList : array : 官网缩略图
                defaultCarModelList : array : 默认车型
                gwDefaultCarModelList : array : 官网默认车型
                price : number : 加价
                sort : number : 排序
                versionDesc : string :
                partsDesc : string : 配件描述
                status : number : 状态 默认启用 1
                type : number : 1:销售版本,2:外观颜色,3:套色,4:内饰颜色,5:选装配置
                params: headers : 请求头
        """
        salesVersionList = self.get_value_choice(salesVersionList, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        optionalList = self.get_value_choice(optionalList, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        appearanceColorList = self.get_value_choice(appearanceColorList, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        interiorColorList = self.get_value_choice(interiorColorList, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        processColorList = self.get_value_choice(processColorList, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_configure.goods_configure_savecarconfigure(**_kwargs)

        self.assert_goods_configure_savecarconfigure(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="查询配置名称-Y")
    def goods_configure_getcarconfigurename(self, modelId="$None$", _assert=True,  **kwargs):
        """
            url=/goods/configure/getCarConfigureName
                params: modelId :  : 车型Id
                params: headers : 请求头
        """
        modelId = self.get_list_choice(modelId, list_or_dict=None, key="modelId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_configure.goods_configure_getcarconfigurename(**_kwargs)

        self.assert_goods_configure_getcarconfigurename(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="车型配置删除-D")
    def goods_configure_removecarconfigure(self, configureId="$None$", _assert=True,  **kwargs):
        """
            url=/goods/configure/removeCarConfigure
                params: configureId :  : 主键Id
                params: headers : 请求头
        """
        configureId = self.get_list_choice(configureId, list_or_dict=None, key="configureId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_configure.goods_configure_removecarconfigure(**_kwargs)

        self.assert_goods_configure_removecarconfigure(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="车型配置更改状态-D")
    def goods_configure_updatecarconfigurestatus(self, configureId="$None$", _assert=True,  **kwargs):
        """
            url=/goods/configure/updateCarConfigureStatus
                params: configureId :  : 车型配置Id
                params: headers : 请求头
        """
        configureId = self.get_list_choice(configureId, list_or_dict=None, key="configureId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_configure.goods_configure_updatecarconfigurestatus(**_kwargs)

        self.assert_goods_configure_updatecarconfigurestatus(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="车型配置查询（930）-?")
    def goods_configure_info(self, modelId="$None$", _assert=True,  **kwargs):
        """
            url=/goods/configure/info
                params: modelId :  : 车型基础ID
                params: headers : 请求头
        """
        modelId = self.get_list_choice(modelId, list_or_dict=None, key="modelId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_configure.goods_configure_info(**_kwargs)

        self.assert_goods_configure_info(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


