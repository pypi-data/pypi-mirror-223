import allure

from service.app_a.asserts.content.asserts_content_adv import AssertsContentAdv
from service.app_a.apis.content import apis_content_adv


class FunsContentAdv(AssertsContentAdv):
    @allure.step(title="点位内容-保存运营端配置(更新、新增)（930）-Y")
    def content_adv_save(self, advId="$None$", advText="$None$", jumpContent="$None$", advLinkUrl="$None$", bindingFlag="$None$", jumpType="$None$", version="$None$", advSerial="$None$", advPlaceId="$None$", advPicUrl="$None$", pictureList="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/adv/save
                params: advPlaceId : number : 左侧列表选中ID
                params: advPicUrl : string : 图片地址
                params: advText : string : 文字描述
                params: advSerial : string : 排序
                params: jumpType : number : 跳转类型
                params: jumpContent : string : 跳转内容
                params: advId : number : 点位ID（更新时必传）
                params: version : string : 绑定的车系（60s,80v）
                params: advLinkUrl : string : 爱车海报填写地址/url跳转地址
                params: bindingFlag : number : 车辆绑定标识 1绑定 0未绑定
                params: pictureList : array : 当跳转类型为16：图片新增字段
                type : string : None
                params: headers : 请求头
        """
        advId = self.get_value_choice(advId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        advText = self.get_value_choice(advText, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        jumpContent = self.get_value_choice(jumpContent, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        advLinkUrl = self.get_value_choice(advLinkUrl, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        bindingFlag = self.get_value_choice(bindingFlag, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        jumpType = self.get_value_choice(jumpType, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        version = self.get_value_choice(version, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        advSerial = self.get_value_choice(advSerial, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        advPlaceId = self.get_value_choice(advPlaceId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        advPicUrl = self.get_value_choice(advPicUrl, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        pictureList = self.get_value_choice(pictureList, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_adv.content_adv_save(**_kwargs)

        self.assert_content_adv_save(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="点位内容-修改点位信息-Y")
    def content_adv_updateessayadvlist(self, essayId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/adv/updateEssayAdvList
                params: essayId : string :
                params: headers : 请求头
        """
        essayId = self.get_value_choice(essayId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_adv.content_adv_updateessayadvlist(**_kwargs)

        self.assert_content_adv_updateessayadvlist(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="点位内容-文章置顶-Y")
    def content_adv_settopflag(self, essayId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/adv/setTopFlag
                params: essayId : text : 文章主键Id
                params: headers : 请求头
        """
        essayId = self.get_value_choice(essayId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_adv.content_adv_settopflag(**_kwargs)

        self.assert_content_adv_settopflag(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="点位内容-点位查询接口-Y")
    def content_adv_advplacelist(self, advPlaceId="$None$", _assert=True,  **kwargs):
        """
            url=/content/adv/advPlaceList
                params: advPlaceId :  : 广告点位主键：
                【发现-推荐】轮播图
                【发现-推荐】快捷入口
                【发现-资讯】金刚区
                【爱车】试驾页轮播
                【发现-推荐】精选内容
                【爱车-智能车控】
                【爱车-购车帮助】
                【我的-邀请好友】海报图
                【我的-积分】积分规则说明
                【爱车-购车帮助（新）】
                params: headers : 请求头
        """
        advPlaceId = self.get_list_choice(advPlaceId, list_or_dict=None, key="advPlaceId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_adv.content_adv_advplacelist(**_kwargs)

        self.assert_content_adv_advplacelist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="点位内容-删除-Y")
    def content_adv_delete(self, advId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/adv/delete
                params: advId : string : 点位ID
                params: headers : 请求头
        """
        advId = self.get_value_choice(advId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_adv.content_adv_delete(**_kwargs)

        self.assert_content_adv_delete(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="点位查询(930版本)-Y")
    def content_adv_detailadmin(self, advPlaceId="$None$", _assert=True,  **kwargs):
        """
            url=/content/adv/detailAdmin
                params: advPlaceId :  : 广告位id
                params: headers : 请求头
        """
        advPlaceId = self.get_list_choice(advPlaceId, list_or_dict=None, key="advPlaceId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_adv.content_adv_detailadmin(**_kwargs)

        self.assert_content_adv_detailadmin(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="点位内容-新增广告位（点位）-Y")
    def content_adv_saveall(self, advPlaceId="$None$", jumpType="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/adv/saveAll
                params: advPlaceId : number : 广告位ID
                params: jumpType : integer : 备注中查看状态信息
                params: headers : 请求头
        """
        advPlaceId = self.get_value_choice(advPlaceId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        jumpType = self.get_value_choice(jumpType, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_adv.content_adv_saveall(**_kwargs)

        self.assert_content_adv_saveall(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="点位内容-根据跳转类型选择跳转内容（930）-Y")
    def content_adv_jumpcontent(self, typeCode="$None$", keyWord="$None$", _assert=True,  **kwargs):
        """
            url=/content/adv/jumpContent
                params: typeCode :  : 跳转类型
                params: keyWord :  :
                params: headers : 请求头
        """
        typeCode = self.get_list_choice(typeCode, list_or_dict=None, key="typeCode")
        keyWord = self.get_list_choice(keyWord, list_or_dict=None, key="keyWord")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_adv.content_adv_jumpcontent(**_kwargs)

        self.assert_content_adv_jumpcontent(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="点位内容-查询推荐页内容-Y")
    def content_adv_detailcontentadmin(self, current=1, orderByCommentCnt="$None$", essayKeyWords="$None$", size=10, _assert=True,  **kwargs):
        """
            url=/content/adv/detailConTentAdmin
                params: current :  :
                params: size :  :
                params: essayKeyWords :  :
                params: orderByCommentCnt :  :
                params: headers : 请求头
        """
        orderByCommentCnt = self.get_list_choice(orderByCommentCnt, list_or_dict=None, key="orderByCommentCnt")
        essayKeyWords = self.get_list_choice(essayKeyWords, list_or_dict=None, key="essayKeyWords")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_adv.content_adv_detailcontentadmin(**_kwargs)

        self.assert_content_adv_detailcontentadmin(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="点位内容-查询跳转类型-Y")
    def content_adv_jumptypelist(self, _assert=True,  **kwargs):
        """
            url=/content/adv/jumpTypeList
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_adv.content_adv_jumptypelist(**_kwargs)

        self.assert_content_adv_jumptypelist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="点位内容-取消推荐-Y")
    def content_adv_cancelrecommend(self, essayId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/adv/cancelRecommend
                params: essayId : string : 文章主键Id
                params: headers : 请求头
        """
        essayId = self.get_value_choice(essayId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_adv.content_adv_cancelrecommend(**_kwargs)

        self.assert_content_adv_cancelrecommend(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="点位-根据点位主键查询点位信息(930版本)")
    def content_adv_detail(self, advPlaceId="$None$", _assert=True,  **kwargs):
        """
            url=/content/adv/detail
                params: advPlaceId :  : 广告点位主键
                1:[发现-推荐]轮播图
                2:[发现-推荐]快捷入口
                5:[发现-资讯]金刚区
                6:[爱车]试驾页轮播
                8:[发现-推荐]精选内容
                9:[爱车-智能车控]
                10:[爱车-购车帮助]
                11:[我的-邀请好友]海报图
                12:[我的-积分]积分规则明细
                params: headers : 请求头
        """
        advPlaceId = self.get_list_choice(advPlaceId, list_or_dict=None, key="advPlaceId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_adv.content_adv_detail(**_kwargs)

        self.assert_content_adv_detail(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


