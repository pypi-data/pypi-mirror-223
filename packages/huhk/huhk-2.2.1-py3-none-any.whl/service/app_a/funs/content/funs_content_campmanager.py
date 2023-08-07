import allure

from service.app_a.asserts.content.asserts_content_campmanager import AssertsContentCampmanager
from service.app_a.apis.content import apis_content_campmanager


class FunsContentCampmanager(AssertsContentCampmanager):
    @allure.step(title="营地服务列表 - 分页查询")
    def content_campmanager_page(self, createBy="$None$", id="$None$", status="$None$", sortBody="$None$", sortord="$None$", name="$None$", _assert=True,  **kwargs):
        """
            url=/content/campManager/page
                params: id :  :
                params: name :  :
                params: status :  :
                params: createBy :  :
                params: sortBody :  :
                params: sortord :  : ASC/DESC/asc/desc
                params: headers : 请求头
        """
        createBy = self.get_list_choice(createBy, list_or_dict=None, key="createBy")
        id = self.get_list_choice(id, list_or_dict=None, key="id")
        status = self.get_list_choice(status, list_or_dict=None, key="status")
        sortBody = self.get_list_choice(sortBody, list_or_dict=None, key="sortBody")
        sortord = self.get_list_choice(sortord, list_or_dict=None, key="sortord")
        name = self.get_list_choice(name, list_or_dict=None, key="name")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_campmanager.content_campmanager_page(**_kwargs)

        self.assert_content_campmanager_page(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="营地列表 - 下架/批量下架")
    def content_campmanager_soldout(self, campId="$None$", id="$None$", _assert=True,  **kwargs):
        """
            url=/content/campManager/soldOut
                params: id :  :
                params: campId : array : 营地服务ID
                type : string : None
                params: headers : 请求头
        """
        campId = self.get_value_choice(campId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        id = self.get_value_choice(id, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_campmanager.content_campmanager_soldout(**_kwargs)

        self.assert_content_campmanager_soldout(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="新增营地 - 新增营地ID带出")
    def content_campmanager_insertcampid(self, _assert=True,  **kwargs):
        """
            url=/content/campManager/insertCampID
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_campmanager.content_campmanager_insertcampid(**_kwargs)

        self.assert_content_campmanager_insertcampid(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="新增营地")
    def content_campmanager_insert(self, content="$None$", id="$None$", county="$None$", url="$None$", province="$None$", city="$None$", campTradeTime="$None$", campDetail="$None$", address="$None$", ownerDiscount="$None$", discountExpEndTime="$None$", discountExpBeginTime="$None$", name="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/campManager/insert
                params: id : text : 营地服务ID
                params: name : text : 营地名称
                params: content : text : 营地简介
                params: url : text : 营地图片
                params: campDetail : text : 营地详情
                params: ownerDiscount : text : 车主优惠
                params: campTradeTime : text : 营地营业时间
                params: discountExpBeginTime : text : 车主优惠有效期 - 开始时间
                params: discountExpEndTime : text : 车主优惠有效期 - 结束时间
                params: province : text : 省
                params: city : text : 市
                params: county : text : 区/县
                params: address : text : 详细地址
                params: headers : 请求头
        """
        content = self.get_value_choice(content, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        id = self.get_value_choice(id, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        county = self.get_value_choice(county, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        url = self.get_value_choice(url, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        province = self.get_value_choice(province, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        city = self.get_value_choice(city, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        campTradeTime = self.get_value_choice(campTradeTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        campDetail = self.get_value_choice(campDetail, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        address = self.get_value_choice(address, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        ownerDiscount = self.get_value_choice(ownerDiscount, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        discountExpEndTime = self.get_value_choice(discountExpEndTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        discountExpBeginTime = self.get_value_choice(discountExpBeginTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        name = self.get_value_choice(name, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_campmanager.content_campmanager_insert(**_kwargs)

        self.assert_content_campmanager_insert(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="营地列表 - 营地详情")
    def content_campmanager_detail_(self, id="$None$", _assert=True,  **kwargs):
        """
            url=/content/campManager/detail/{id}
                params: id :  : 营地服务ID
                params: headers : 请求头
        """
        id = self.get_list_choice(id, list_or_dict=None, key="id")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_campmanager.content_campmanager_detail_(**_kwargs)

        self.assert_content_campmanager_detail_(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="编辑营地")
    def content_campmanager_update(self, phone="$None$", areaCode="$None$", ownerDiscount="$None$", discountExpEndTime="$None$", discountExpBeginTime="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/campManager/update
                params: ownerDiscount : text : 车主优惠
                params: discountExpBeginTime : text : 车主优惠有效期 - 开始时间
                params: discountExpEndTime : text : 车主优惠有效期 - 结束时间
                params: areaCode : text : 区号
                params: phone : text : 手机号
                params: headers : 请求头
        """
        phone = self.get_value_choice(phone, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        areaCode = self.get_value_choice(areaCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        ownerDiscount = self.get_value_choice(ownerDiscount, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        discountExpEndTime = self.get_value_choice(discountExpEndTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        discountExpBeginTime = self.get_value_choice(discountExpBeginTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_campmanager.content_campmanager_update(**_kwargs)

        self.assert_content_campmanager_update(_assert, **_kwargs)
        self.set_value(_kwargs)


