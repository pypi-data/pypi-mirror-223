import allure

from service.app_a.asserts.content.asserts_content_agreement import AssertsContentAgreement
from service.app_a.apis.content import apis_content_agreement


class FunsContentAgreement(AssertsContentAgreement):
    @allure.step(title="查询创建活动所需协议")
    def content_agreement_getagreement(self, _assert=True,  **kwargs):
        """
            url=/content/agreement/getAgreement
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_agreement.content_agreement_getagreement(**_kwargs)

        self.assert_content_agreement_getagreement(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="协议-C端用户根据编码查询协议-Y")
    def content_agreement_getbycode(self, agreementCode="$None$", _assert=True,  **kwargs):
        """
            url=/content/agreement/getByCode
                params: agreementCode :  : PRIVACYPOLICY:隐私协议，USERPOLICY：用户协议， THIRDPARTYSDKPOLICY：第三方sdk目录，POINTRULE：积分规则，SIGININRULE：签到规则
                params: headers : 请求头
        """
        agreementCode = self.get_list_choice(agreementCode, list_or_dict=None, key="agreementCode")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_agreement.content_agreement_getbycode(**_kwargs)

        self.assert_content_agreement_getbycode(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="协议-h5查询协议-Y")
    def content_agreement_getagreementbycode(self, agreementCode="$None$", _assert=True,  **kwargs):
        """
            url=/content/agreement/getAgreementByCode
                params: agreementCode :  : 协议编码
                隐私协议:PRIVACYPOLICY、
                用户协议:USERPOLICY、
                权限清单:PERMISSIONSLIST、
                第三方SDK列表:THIRDPARTYSDKPOLICY、
                用户注销: USERDESTROY
                车机服务协议: CARSERVICE
                params: headers : 请求头
        """
        agreementCode = self.get_list_choice(agreementCode, list_or_dict=None, key="agreementCode")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_agreement.content_agreement_getagreementbycode(**_kwargs)

        self.assert_content_agreement_getagreementbycode(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="协议-停用启用协议-Y")
    def content_agreement_updatestatus(self, agreementId="$None$", status="$None$", code="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/agreement/updateStatus
                params: agreementId : text :
                params: status : text : 状态 1 启用 2 停用
                params: code : text : 协议编码
                params: headers : 请求头
        """
        agreementId = self.get_value_choice(agreementId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        status = self.get_value_choice(status, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        code = self.get_value_choice(code, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_agreement.content_agreement_updatestatus(**_kwargs)

        self.assert_content_agreement_updatestatus(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="协议-协议列表-Y")
    def content_agreement_list(self, current=1, size=10, _assert=True,  **kwargs):
        """
            url=/content/agreement/list
                params: size :  : 每页数据数
                params: current :  : 当前页
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_agreement.content_agreement_list(**_kwargs)

        self.assert_content_agreement_list(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="协议-新增协议-Y")
    def content_agreement_save(self, content="$None$", version="$None$", name="$None$", code="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/agreement/save
                params: name : string : 协议名
                params: content : string : 内容
                params: version : number : 版本号
                params: code : string : 协议编码
                params: headers : 请求头
        """
        content = self.get_value_choice(content, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        version = self.get_value_choice(version, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        name = self.get_value_choice(name, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        code = self.get_value_choice(code, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_agreement.content_agreement_save(**_kwargs)

        self.assert_content_agreement_save(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="协议-更新协议-Y")
    def content_agreement_update(self, content="$None$", version="$None$", code="$None$", agreementId="$None$", name="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/agreement/update
                params: name : string : 协议名
                params: content : string : 内容
                params: version : number : 版本号
                params: agreementId : string : 协议id
                params: code : string : 协议编码
                params: headers : 请求头
        """
        content = self.get_value_choice(content, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        version = self.get_value_choice(version, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        code = self.get_value_choice(code, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        agreementId = self.get_value_choice(agreementId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        name = self.get_value_choice(name, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_agreement.content_agreement_update(**_kwargs)

        self.assert_content_agreement_update(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="协议-根据id获取详情-Y")
    def content_agreement_getbyid(self, agreementId="$None$", _assert=True,  **kwargs):
        """
            url=/content/agreement/getById
                params: agreementId :  : 协议主键1-隐私协议2-用户协议3-第三方SDK目录
                params: headers : 请求头
        """
        agreementId = self.get_list_choice(agreementId, list_or_dict=None, key="agreementId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_agreement.content_agreement_getbyid(**_kwargs)

        self.assert_content_agreement_getbyid(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


