import allure

from service.app_a.asserts.content.asserts_content_contentmanager import AssertsContentContentmanager
from service.app_a.apis.content import apis_content_contentmanager


class FunsContentContentmanager(AssertsContentContentmanager):
    @allure.step(title="动态-评论列表-Y")
    def content_contentmanager_commentlist(self, current=1, size=10, contentId="$None$", _assert=True,  **kwargs):
        """
            url=/content/contentManager/commentList
                params: contentId :  : 动态主键
                params: size :  : 每页数据数
                params: current :  : 当前页
                params: headers : 请求头
        """
        contentId = self.get_list_choice(contentId, list_or_dict=None, key="contentId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_contentmanager.content_contentmanager_commentlist(**_kwargs)

        self.assert_content_contentmanager_commentlist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


