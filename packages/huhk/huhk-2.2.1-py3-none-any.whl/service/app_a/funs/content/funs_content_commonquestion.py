import allure

from service.app_a.asserts.content.asserts_content_commonquestion import AssertsContentCommonquestion
from service.app_a.apis.content import apis_content_commonquestion


class FunsContentCommonquestion(AssertsContentCommonquestion):
    @allure.step(title="常见问题-上下架-Y")
    def content_commonquestion_updatestatus(self, essayId="$None$", status="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/commonquestion/updateStatus
                params: essayId :  : 主键id
                params: status : string : 上架2 下架3
                params: headers : 请求头
        """
        essayId = self.get_value_choice(essayId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        status = self.get_value_choice(status, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_commonquestion.content_commonquestion_updatestatus(**_kwargs)

        self.assert_content_commonquestion_updatestatus(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="常见问题-修改-Y")
    def content_commonquestion_update(self, content="$None$", essayId="$None$", title="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/commonquestion/update
                params: essayId :  : 主键id
                params: title : string : 标题
                params: content : string : 内容
                params: headers : 请求头
        """
        content = self.get_value_choice(content, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        essayId = self.get_value_choice(essayId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        title = self.get_value_choice(title, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_commonquestion.content_commonquestion_update(**_kwargs)

        self.assert_content_commonquestion_update(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="常见问题-修改权重-Y")
    def content_commonquestion_updaterank(self, essayId="$None$", rank="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/commonquestion/updateRank
                params: essayId :  : 主键id
                params: rank : string : 权重
                params: headers : 请求头
        """
        essayId = self.get_value_choice(essayId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        rank = self.get_value_choice(rank, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_commonquestion.content_commonquestion_updaterank(**_kwargs)

        self.assert_content_commonquestion_updaterank(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="常见问题-删除-Y")
    def content_commonquestion_delete(self, essayId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/commonquestion/delete
                params: essayId :  : 主键id
                params: headers : 请求头
        """
        essayId = self.get_value_choice(essayId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_commonquestion.content_commonquestion_delete(**_kwargs)

        self.assert_content_commonquestion_delete(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="常见问题-后台列表-Y")
    def content_commonquestion_list(self, current=1, size=10, _assert=True,  **kwargs):
        """
            url=/content/commonquestion/list
                params: current :  : 当前页数
                params: size :  : 每页个数
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_commonquestion.content_commonquestion_list(**_kwargs)

        self.assert_content_commonquestion_list(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="常见问题-已发布列表-Y")
    def content_commonquestion_publishlist(self, current=1, size=10, _assert=True,  **kwargs):
        """
            url=/content/commonquestion/publishList
                params: current :  : 当前页数
                params: size :  : 每页数量
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_commonquestion.content_commonquestion_publishlist(**_kwargs)

        self.assert_content_commonquestion_publishlist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="常见问题-新增-Y")
    def content_commonquestion_add(self, content="$None$", essayId="$None$", title="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/commonquestion/add
                params: essayId :  : 主键id
                params: title : string : 标题
                params: content : string : 内容
                params: headers : 请求头
        """
        content = self.get_value_choice(content, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        essayId = self.get_value_choice(essayId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        title = self.get_value_choice(title, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_commonquestion.content_commonquestion_add(**_kwargs)

        self.assert_content_commonquestion_add(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="常见问题-生成id-Y")
    def content_commonquestion_createid(self, _assert=True,  **kwargs):
        """
            url=/content/commonquestion/createId
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_commonquestion.content_commonquestion_createid(**_kwargs)

        self.assert_content_commonquestion_createid(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="常见问题-详情-Y")
    def content_commonquestion_info(self, essayId="$None$", _assert=True,  **kwargs):
        """
            url=/content/commonquestion/info
                params: essayId :  : 主键id
                params: headers : 请求头
        """
        essayId = self.get_list_choice(essayId, list_or_dict=None, key="essayId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_commonquestion.content_commonquestion_info(**_kwargs)

        self.assert_content_commonquestion_info(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


