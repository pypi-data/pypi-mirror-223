import allure

from service.app_a.asserts.content.asserts_content_safecode import AssertsContentSafecode
from service.app_a.apis.content import apis_content_safecode


class FunsContentSafecode(AssertsContentSafecode):
    @allure.step(title="安全码关闭-Y")
    def content_safecode_close(self, safeCode="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/safeCode/close
                params: safeCode : string : 安全码
                params: headers : 请求头
        """
        safeCode = self.get_value_choice(safeCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_safecode.content_safecode_close(**_kwargs)

        self.assert_content_safecode_close(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="安全码新增-Y")
    def content_safecode_add(self, safeCode="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/safeCode/add
                params: safeCode : string : 安全码
                params: headers : 请求头
        """
        safeCode = self.get_value_choice(safeCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_safecode.content_safecode_add(**_kwargs)

        self.assert_content_safecode_add(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="安全码校验-Y")
    def content_safecode_verify(self, safeCode="$None$", _assert=True,  **kwargs):
        """
            url=/content/safeCode/verify
                params: safeCode :  : 安全码
                params: headers : 请求头
        """
        safeCode = self.get_list_choice(safeCode, list_or_dict=None, key="safeCode")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_safecode.content_safecode_verify(**_kwargs)

        self.assert_content_safecode_verify(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="安全码状态查询-Y")
    def content_safecode_getstatus(self, _assert=True,  **kwargs):
        """
            url=/content/safeCode/getStatus
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_safecode.content_safecode_getstatus(**_kwargs)

        self.assert_content_safecode_getstatus(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="安全码重置-Y")
    def content_safecode_reset(self, safeCode="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/safeCode/reset
                params: safeCode : string : 安全码
                params: headers : 请求头
        """
        safeCode = self.get_value_choice(safeCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_safecode.content_safecode_reset(**_kwargs)

        self.assert_content_safecode_reset(_assert, **_kwargs)
        self.set_value(_kwargs)


