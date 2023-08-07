import allure

from service.app_a.asserts.content.asserts_content_topic4c import AssertsContentTopic4C
from service.app_a.apis.content import apis_content_topic4c


class FunsContentTopic4C(AssertsContentTopic4C):
    @allure.step(title="话题-删除话题")
    def content_topic4c_del(self, topicId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/topic4C/del
                params: topicId : string : 话题主键
                params: headers : 请求头
        """
        topicId = self.get_value_choice(topicId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_topic4c.content_topic4c_del(**_kwargs)

        self.assert_content_topic4c_del(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="话题-获取动态关联列表-Y")
    def content_topic4c_getcontentlist(self, topicId="$None$", current=1, size=10, _assert=True,  **kwargs):
        """
            url=/content/topic4C/getContentList
                params: topicId :  : 话题主键
                params: size :  : 每页数据数
                params: current :  : 当前页
                params: headers : 请求头
        """
        topicId = self.get_list_choice(topicId, list_or_dict=None, key="topicId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_topic4c.content_topic4c_getcontentlist(**_kwargs)

        self.assert_content_topic4c_getcontentlist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="话题-搜索话题列表")
    def content_topic4c_list(self, createBy="$None$", topicId="$None$", current=1, keyWord="$None$", startTime="$None$", endTime="$None$", size=10, _assert=True,  **kwargs):
        """
            url=/content/topic4C/list
                params: topicId :  : 话题主键
                params: createBy :  : 发布人主键
                params: keyWord :  : 话题关键字
                params: startTime :  : 搜索开始时间
                params: endTime :  : 搜索结束时间
                params: size :  : 每页数量数
                params: current :  : 当前页
                params: headers : 请求头
        """
        createBy = self.get_list_choice(createBy, list_or_dict=None, key="createBy")
        topicId = self.get_list_choice(topicId, list_or_dict=None, key="topicId")
        keyWord = self.get_list_choice(keyWord, list_or_dict=None, key="keyWord")
        startTime = self.get_list_choice(startTime, list_or_dict=None, key="startTime")
        endTime = self.get_list_choice(endTime, list_or_dict=None, key="endTime")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_topic4c.content_topic4c_list(**_kwargs)

        self.assert_content_topic4c_list(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="话题-新增话题")
    def content_topic4c_insert(self, topicId="$None$", author="$None$", topicTitle="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/topic4C/insert
                params: topicId : string : 话题主键
                params: topicTitle : string : 话题
                params: author : number : 话题作者
                params: headers : 请求头
        """
        topicId = self.get_value_choice(topicId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        author = self.get_value_choice(author, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        topicTitle = self.get_value_choice(topicTitle, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_topic4c.content_topic4c_insert(**_kwargs)

        self.assert_content_topic4c_insert(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="话题-置顶")
    def content_topic4c_top(self, topicId="$None$", type="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/topic4C/top
                params: topicId : string : 话题主键
                params: type : string : 操作类型1：置顶2：取消置顶
                params: headers : 请求头
        """
        topicId = self.get_value_choice(topicId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        type = self.get_value_choice(type, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_topic4c.content_topic4c_top(**_kwargs)

        self.assert_content_topic4c_top(_assert, **_kwargs)
        self.set_value(_kwargs)


