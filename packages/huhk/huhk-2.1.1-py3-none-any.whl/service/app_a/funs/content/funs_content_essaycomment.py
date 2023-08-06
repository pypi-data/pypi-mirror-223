import allure

from service.app_a.asserts.content.asserts_content_essaycomment import AssertsContentEssaycomment
from service.app_a.apis.content import apis_content_essaycomment


class FunsContentEssaycomment(AssertsContentEssaycomment):
    @allure.step(title="后台管理-新建评论/回复1030-Y")
    def content_essaycomment_manageadd(self, author="$None$", essayId="$None$", parentId="$None$", content="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/essaycomment/manageAdd
                params: essayId : string : 文章id
                params: author : string : 评论人id
                params: content : string : 内容
                params: parentId : string : 所回复评论的id 新建评论不用传 回复要传
                params: headers : 请求头
        """
        author = self.get_value_choice(author, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        essayId = self.get_value_choice(essayId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        parentId = self.get_value_choice(parentId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        content = self.get_value_choice(content, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_essaycomment.content_essaycomment_manageadd(**_kwargs)

        self.assert_content_essaycomment_manageadd(_assert, **_kwargs)
        self.set_value(_kwargs)


