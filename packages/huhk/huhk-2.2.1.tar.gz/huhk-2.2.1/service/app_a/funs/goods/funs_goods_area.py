import allure

from service.app_a.asserts.goods.asserts_goods_area import AssertsGoodsArea
from service.app_a.apis.goods import apis_goods_area


class FunsGoodsArea(AssertsGoodsArea):
    @allure.step(title="订单管理-地区下拉（930版本）-Y")
    def goods_area_getparentarea(self, parentId="$None$", country="$None$", _assert=True,  **kwargs):
        """
            url=/goods/area/getParentArea
                params: parentId :  : 父地区id（null 则省，下一级递增）
                params: country :  : all会加上全国信息
                params: headers : 请求头
        """
        parentId = self.get_list_choice(parentId, list_or_dict=None, key="parentId")
        country = self.get_list_choice(country, list_or_dict=None, key="country")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_area.goods_area_getparentarea(**_kwargs)

        self.assert_goods_area_getparentarea(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="pc端查询城市默认经销商-Y")
    def goods_area_getdefaultdealer(self, cityCode="$None$", _assert=True,  **kwargs):
        """
            url=/goods/area/getDefaultDealer
                params: cityCode :  : 城市编码
                params: headers : 请求头
        """
        cityCode = self.get_list_choice(cityCode, list_or_dict=None, key="cityCode")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_area.goods_area_getdefaultdealer(**_kwargs)

        self.assert_goods_area_getdefaultdealer(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="后台管理-设置默认经销商-Y")
    def goods_area_insertrelation(self, areaIds="$None$", dealerCode="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/goods/area/insertRelation
                params: areaIds : array : 地区集合
                type : integer : None
                description : 地区Id : None
                params: dealerCode : string : 进销商编码
                params: headers : 请求头
        """
        areaIds = self.get_value_choice(areaIds, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        dealerCode = self.get_value_choice(dealerCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_area.goods_area_insertrelation(**_kwargs)

        self.assert_goods_area_insertrelation(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="城市禁行列表查询-Y")
    def goods_area_getcitylist(self, cName="$None$", current=1, pName="$None$", cType="$None$", size=10, _assert=True,  **kwargs):
        """
            url=/goods/area/getCityList
                params: size :  : 当前页数量
                params: current :  : 当前页号
                params: pName :  : 省份名称
                params: cName :  : 城市名称
                params: cType :  : 城市禁行类型 0:全面解禁，1:部分解禁，2:禁行
                params: headers : 请求头
        """
        cName = self.get_list_choice(cName, list_or_dict=None, key="cName")
        pName = self.get_list_choice(pName, list_or_dict=None, key="pName")
        cType = self.get_list_choice(cType, list_or_dict=None, key="cType")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_area.goods_area_getcitylist(**_kwargs)

        self.assert_goods_area_getcitylist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="查询禁行城市信息-Y")
    def goods_area_getcitybyid(self, cityId="$None$", _assert=True,  **kwargs):
        """
            url=/goods/area/getCityById
                params: cityId :  : 城市编码
                params: headers : 请求头
        """
        cityId = self.get_list_choice(cityId, list_or_dict=None, key="cityId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_area.goods_area_getcitybyid(**_kwargs)

        self.assert_goods_area_getcitybyid(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="地区下拉待字母（930）-?")
    def goods_area_getmaparea(self, parentId="$None$", _assert=True,  **kwargs):
        """
            url=/goods/area/getMapArea
                params: parentId :  : 地区Id（省传null ，其余传areaId的值）
                params: headers : 请求头
        """
        parentId = self.get_list_choice(parentId, list_or_dict=None, key="parentId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_area.goods_area_getmaparea(**_kwargs)

        self.assert_goods_area_getmaparea(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="城市下拉带字母（930）-？")
    def goods_area_getcity(self, parentId="$None$", _assert=True,  **kwargs):
        """
            url=/goods/area/getCity
                params: parentId :  : 父级ID
                params: headers : 请求头
        """
        parentId = self.get_list_choice(parentId, list_or_dict=None, key="parentId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_area.goods_area_getcity(**_kwargs)

        self.assert_goods_area_getcity(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="城市禁行状态变更-？")
    def goods_area_updatecitytype(self, cType="$None$", cId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/goods/area/updateCityType
                params: cType : integer : 禁用类型
                params: cId : integer : 城市编码
                params: headers : 请求头
        """
        cType = self.get_value_choice(cType, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        cId = self.get_value_choice(cId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_goods_area.goods_area_updatecitytype(**_kwargs)

        self.assert_goods_area_updatecitytype(_assert, **_kwargs)
        self.set_value(_kwargs)


