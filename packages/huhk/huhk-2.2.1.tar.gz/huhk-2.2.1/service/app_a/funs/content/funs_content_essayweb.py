import allure

from service.app_a.asserts.content.asserts_content_essayweb import AssertsContentEssayweb
from service.app_a.apis.content import apis_content_essayweb


class FunsContentEssayweb(AssertsContentEssayweb):
    @allure.step(title="专题-后台官网专题新建文章-Y")
    def content_essayweb_add(self, essPicUrl="$None$", content="$None$", publishType="$None$", title="$None$", author="$None$", status="$None$", publishTime="$None$", essayId="$None$", publishChannel="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/essayweb/add
                params: essayId : string : 文章主键
                params: title : string : 文章标题
                params: author : string : 作者
                params: publishType : string : 发布类型1：立即发布2：定时发布
                params: publishTime : string : 定时发布时间
                params: essPicUrl : string : 文章封面
                params: publishChannel : string : 发布渠道
                params: content : string : 文章正文富文本
                params: status : string : 保存时传1，提交审核时传2
                params: headers : 请求头
        """
        essPicUrl = self.get_value_choice(essPicUrl, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        content = self.get_value_choice(content, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        publishType = self.get_value_choice(publishType, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        title = self.get_value_choice(title, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        author = self.get_value_choice(author, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        status = self.get_value_choice(status, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        publishTime = self.get_value_choice(publishTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        essayId = self.get_value_choice(essayId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        publishChannel = self.get_value_choice(publishChannel, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_essayweb.content_essayweb_add(**_kwargs)

        self.assert_content_essayweb_add(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="专题-后台官网文章关键词搜索-Y")
    def content_essayweb_searchbykey(self, key="$None$", current=1, size=10, _assert=True,  **kwargs):
        """
            url=/content/essayweb/searchByKey
                params: current :  : 当前页
                params: size :  : 每页条数
                params: key :  : 关键词
                params: headers : 请求头
        """
        key = self.get_list_choice(key, list_or_dict=None, key="key")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_essayweb.content_essayweb_searchbykey(**_kwargs)

        self.assert_content_essayweb_searchbykey(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="专题-后台官网文章删除-Y")
    def content_essayweb_delete_(self, essayId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/essayweb/delete/{essayId}
                params: essayId :  : 文章id
                params: headers : 请求头
        """
        essayId = self.get_value_choice(essayId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_essayweb.content_essayweb_delete_(**_kwargs)

        self.assert_content_essayweb_delete_(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="新闻中心查看文章详情-Y")
    def content_essayweb_getbyid(self, essayId="$None$", subjectId="$None$", _assert=True,  **kwargs):
        """
            url=/content/essayweb/getById
                params: essayId :  : 文章主键
                params: subjectId :  :
                params: headers : 请求头
        """
        essayId = self.get_list_choice(essayId, list_or_dict=None, key="essayId")
        subjectId = self.get_list_choice(subjectId, list_or_dict=None, key="subjectId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_essayweb.content_essayweb_getbyid(**_kwargs)

        self.assert_content_essayweb_getbyid(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


