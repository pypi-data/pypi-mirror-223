import allure

from service.app_a.asserts.goods.asserts_goods_carmodel import AssertsGoodsCarmodel
from service.app_a.apis.goods import apis_goods_carmodel


class FunsGoodsCarmodel(AssertsGoodsCarmodel):
    @allure.step(title="保存车型详细信息 - Y")
    def goods_carmodel_savemanagecarmodel(self, prePricePosters="$None$", modelCode="$None$", price="$None$", status="$None$", posters="$None$", preEndTime="$None$", modelName="$None$", promptDesc="$None$", prePrice="$None$", carDetailPics="$None$", preToDepositEndTime="$None$", depositStartTime="$None$", carSimpleName="$None$", depositPrice="$None$", sharePosters="$None$", brandName="$None$", preStartTime="$None$", depositPriceContent="$None$", version="$None$", carName="$None$", configCode="$None$", depositEndTime="$None$", prePriceContent="$None$", preToDepositStartTime="$None$", modelId="$None$", carCode="$None$", carDetailType="$None$", carDetailUrl="$None$", sort="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/goods/carmodel/saveManageCarModel
                params: carName : string : 车系名称
                params: brandName : string : 品牌名称
                params: version : string : 品牌代码
                params: carCode : string : 车系代码
                params: modelName : string : 车型名称
                params: modelCode : string : 车型代号
                params: carSimpleName : string : 车型销售名称
                params: configCode : string : 配置编码
                params: sort : number : 车型权重
                params: price : number : 基础零售价
                params: carDetailType : number : 车型详情类型 - 1:图片，2:H5连接
                params: carDetailUrl : string : 车型详情类型为2 h5跳转地址
                params: preStartTime : string : 预订开始时间
                params: preEndTime : string : 预订结束时间
                params: preToDepositStartTime : string : 预订转大定开始时间
                params: preToDepositEndTime : string : 预订转大定结束时间
                params: prePrice : number : 预订金价格
                params: prePriceContent : string : 预订权益内容
                params: depositStartTime : string : 大定开始时间
                params: depositEndTime : string : 大定结束时间
                params: depositPrice : number : 定金价格
                params: depositPriceContent : string : 定金权益内容
                params: posters : array : 爱车海报
                imageUrl : string : 图片地址
                modelId : string : 车型ID
                params: sharePosters : array : 分享海报
                imageUrl : string :
                modelId : string :
                params: carDetailPics : array : 车详情图片
                imageUrl : string :
                modelId : string :
                params: prePricePosters : array : 预订金海报
                imageUrl : string :
                modelId : string :
                params: promptDesc : string : 提示文案
                params: modelId : string : 车型ID
                params: status : number : 状态(0禁用1启用)
                params: headers : 请求头
        """
        prePricePosters = self.get_value_choice(prePricePosters, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        modelCode = self.get_value_choice(modelCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        price = self.get_value_choice(price, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        status = self.get_value_choice(status, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        posters = self.get_value_choice(posters, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        preEndTime = self.get_value_choice(preEndTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        modelName = self.get_value_choice(modelName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        promptDesc = self.get_value_choice(promptDesc, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        prePrice = self.get_value_choice(prePrice, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        carDetailPics = self.get_value_choice(carDetailPics, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        preToDepositEndTime = self.get_value_choice(preToDepositEndTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        depositStartTime = self.get_value_choice(depositStartTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        carSimpleName = self.get_value_choice(carSimpleName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        depositPrice = self.get_value_choice(depositPrice, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        sharePosters = self.get_value_choice(sharePosters, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        brandName = self.get_value_choice(brandName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        preStartTime = self.get_value_choice(preStartTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        depositPriceContent = self.get_value_choice(depositPriceContent, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        version = self.get_value_choice(version, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        carName = self.get_value_choice(carName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        configCode = self.get_value_choice(configCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        depositEndTime = self.get_value_choice(depositEndTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        prePriceContent = self.get_value_choice(prePriceContent, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        preToDepositStartTime = self.get_value_choice(preToDepositStartTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        modelId = self.get_value_choice(modelId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        carCode = self.get_value_choice(carCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        carDetailType = self.get_value_choice(carDetailType, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        carDetailUrl = self.get_value_choice(carDetailUrl, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        sort = self.get_value_choice(sort, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_carmodel.goods_carmodel_savemanagecarmodel(**_kwargs)

        self.assert_goods_carmodel_savemanagecarmodel(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="删除车型-Y")
    def goods_carmodel_removebyid(self, modelId="$None$", _assert=True,  **kwargs):
        """
            url=/goods/carmodel/removeById
                params: modelId :  : 车型id
                params: headers : 请求头
        """
        modelId = self.get_list_choice(modelId, list_or_dict=None, key="modelId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_carmodel.goods_carmodel_removebyid(**_kwargs)

        self.assert_goods_carmodel_removebyid(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="查询车型详细信息-Y")
    def goods_carmodel_getcarmodelmanagebyid(self, modelId="$None$", _assert=True,  **kwargs):
        """
            url=/goods/carmodel/getCarModelManageById
                params: modelId :  : 车型编码
                params: headers : 请求头
        """
        modelId = self.get_list_choice(modelId, list_or_dict=None, key="modelId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_carmodel.goods_carmodel_getcarmodelmanagebyid(**_kwargs)

        self.assert_goods_carmodel_getcarmodelmanagebyid(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="车型列表-Y")
    def goods_carmodel_getmanagecarmodel(self, carName="$None$", modelCode="$None$", brandName="$None$", current=1, status="$None$", carCode="$None$", version="$None$", operator="$None$", modelName="$None$", size=10, _assert=True,  **kwargs):
        """
            url=/goods/carmodel/getManageCarModel
                params: current :  : 分页
                params: size :  : 分页
                params: modelName :  : 车型名称
                params: modelCode :  : 车型代号
                params: status :  : 0:待启用，1:启用，2:禁用 车型新增默认状态待启用，全部则不传值
                params: operator :  : 操作人
                params: brandName :  : 品牌名称
                params: version :  : 品牌编码
                params: carName :  : 车系名称
                params: carCode :  : 车型编码
                params: headers : 请求头
        """
        carName = self.get_list_choice(carName, list_or_dict=None, key="carName")
        modelCode = self.get_list_choice(modelCode, list_or_dict=None, key="modelCode")
        brandName = self.get_list_choice(brandName, list_or_dict=None, key="brandName")
        status = self.get_list_choice(status, list_or_dict=None, key="status")
        carCode = self.get_list_choice(carCode, list_or_dict=None, key="carCode")
        version = self.get_list_choice(version, list_or_dict=None, key="version")
        operator = self.get_list_choice(operator, list_or_dict=None, key="operator")
        modelName = self.get_list_choice(modelName, list_or_dict=None, key="modelName")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_carmodel.goods_carmodel_getmanagecarmodel(**_kwargs)

        self.assert_goods_carmodel_getmanagecarmodel(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="订单管理-查询可试驾车型-Y")
    def goods_carmodel_getmodelnamelist(self, _assert=True,  **kwargs):
        """
            url=/goods/carmodel/getModelNameList
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_carmodel.goods_carmodel_getmodelnamelist(**_kwargs)

        self.assert_goods_carmodel_getmodelnamelist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="车型下拉列表-Y")
    def goods_carmodel_getcarnamelist(self, _assert=True,  **kwargs):
        """
            url=/goods/carmodel/getCarNameList
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_carmodel.goods_carmodel_getcarnamelist(**_kwargs)

        self.assert_goods_carmodel_getcarnamelist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


