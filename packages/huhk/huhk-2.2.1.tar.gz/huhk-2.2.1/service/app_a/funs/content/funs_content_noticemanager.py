import allure

from service.app_a.asserts.content.asserts_content_noticemanager import AssertsContentNoticemanager
from service.app_a.apis.content import apis_content_noticemanager


class FunsContentNoticemanager(AssertsContentNoticemanager):
    @allure.step(title="系统通知列表查询接口-Y")
    def content_noticemanager_page(self, _assert=True,  **kwargs):
        """
            url=/content/noticeManager/page
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_noticemanager.content_noticemanager_page(**_kwargs)

        self.assert_content_noticemanager_page(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="获取系统通知详情")
    def content_noticemanager_getnoticeparamslist_(self, templateType="$None$", messageId="$None$", _assert=True,  **kwargs):
        """
            url=/content/noticeManager/getNoticeParamsList/{messageId}
                params: messageId :  :
                params: templateType :  : 模板编码
                params: headers : 请求头
        """
        templateType = self.get_list_choice(templateType, list_or_dict=None, key="templateType")
        messageId = self.get_list_choice(messageId, list_or_dict=None, key="messageId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_noticemanager.content_noticemanager_getnoticeparamslist_(**_kwargs)

        self.assert_content_noticemanager_getnoticeparamslist_(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="系统通知变量编辑-Y")
    def content_noticemanager_noticeparamsupdate(self, templateType="$None$", templateName="$None$", templateContent="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/noticeManager/noticeParamsUpdate
                params: templateType : string : 模板类型
                params: templateName : string : 模板名称（标题）
                params: templateContent : string : 模板内容
                params: headers : 请求头
        """
        templateType = self.get_value_choice(templateType, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        templateName = self.get_value_choice(templateName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        templateContent = self.get_value_choice(templateContent, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_noticemanager.content_noticemanager_noticeparamsupdate(**_kwargs)

        self.assert_content_noticemanager_noticeparamsupdate(_assert, **_kwargs)
        self.set_value(_kwargs)


