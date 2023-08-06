import allure

from service.app_a.asserts.content.asserts_content_subjectweb import AssertsContentSubjectweb
from service.app_a.apis.content import apis_content_subjectweb


class FunsContentSubjectweb(AssertsContentSubjectweb):
    @allure.step(title="专题-后台官网专题文章列表-Y")
    def content_subjectweb_detailessay(self, current=1, subjectId="$None$", size=10, _assert=True,  **kwargs):
        """
            url=/content/subjectweb/detailEssay
                params: current :  : 当前页
                params: size :  : 当前条数
                params: subjectId :  : 专题主键id
                params: headers : 请求头
        """
        subjectId = self.get_list_choice(subjectId, list_or_dict=None, key="subjectId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_subjectweb.content_subjectweb_detailessay(**_kwargs)

        self.assert_content_subjectweb_detailessay(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="专题-后台官网专题新增-Y")
    def content_subjectweb_add(self, isService="$None$", isSearch="$None$", subPicUrl="$None$", subjectName="$None$", explain="$None$", parentId="$None$", web="$None$", status="$None$", level="$None$", siftFlag="$None$", recommend="$None$", serial="$None$", subjectRank="$None$", type="$None$", siftPicUrl="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/subjectweb/add
                params: subjectName : string : 专题名称
                params: level : string : 专题等级
                params: status : string : 是否可用1：是 0：否
                params: explain : string : 说明
                params: type : string : 关联类型
                params: subPicUrl : string : 专题图片
                params: parentId : string : 父级专题主键
                params: serial : integer : 序号
                params: siftFlag : integer : 精选标识 0否 1是
                params: isService : integer : 是否有客服入口 0否 1是
                params: isSearch : integer : 是否配置搜索 0否 1是
                params: siftPicUrl : string : 精选配图
                params: web : string :
                params: recommend : integer : 咨询页展示
                params: subjectRank : integer : 精选权重
                params: headers : 请求头
        """
        isService = self.get_value_choice(isService, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        isSearch = self.get_value_choice(isSearch, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        subPicUrl = self.get_value_choice(subPicUrl, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        subjectName = self.get_value_choice(subjectName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        explain = self.get_value_choice(explain, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        parentId = self.get_value_choice(parentId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        web = self.get_value_choice(web, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        status = self.get_value_choice(status, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        level = self.get_value_choice(level, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        siftFlag = self.get_value_choice(siftFlag, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        recommend = self.get_value_choice(recommend, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        serial = self.get_value_choice(serial, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        subjectRank = self.get_value_choice(subjectRank, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        type = self.get_value_choice(type, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        siftPicUrl = self.get_value_choice(siftPicUrl, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_subjectweb.content_subjectweb_add(**_kwargs)

        self.assert_content_subjectweb_add(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="专题-后台官网专题类型列表-Y")
    def content_subjectweb_treelist(self, _assert=True,  **kwargs):
        """
            url=/content/subjectweb/treeList
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_subjectweb.content_subjectweb_treelist(**_kwargs)

        self.assert_content_subjectweb_treelist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="专题-后台官网保存/更新-Y")
    def content_subjectweb_save(self, delFlag="$None$", isService="$None$", isSearch="$None$", subPicUrl="$None$", subjectName="$None$", explain="$None$", parentId="$None$", status="$None$", siftFlag="$None$", subjectId="$None$", type="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/subjectweb/save
                params: subjectId : string :
                params: subjectName : string :
                params: delFlag : string :
                params: subPicUrl : string :
                params: explain : string :
                params: status : string :
                params: type : string :
                params: parentId : string :
                params: siftFlag : string :
                params: isService : string :
                params: isSearch : string :
                params: headers : 请求头
        """
        delFlag = self.get_value_choice(delFlag, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        isService = self.get_value_choice(isService, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        isSearch = self.get_value_choice(isSearch, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        subPicUrl = self.get_value_choice(subPicUrl, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        subjectName = self.get_value_choice(subjectName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        explain = self.get_value_choice(explain, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        parentId = self.get_value_choice(parentId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        status = self.get_value_choice(status, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        siftFlag = self.get_value_choice(siftFlag, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        subjectId = self.get_value_choice(subjectId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        type = self.get_value_choice(type, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_subjectweb.content_subjectweb_save(**_kwargs)

        self.assert_content_subjectweb_save(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="专题-后台官网删除专题-Y")
    def content_subjectweb_del(self, subjectId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/subjectweb/del
                params: subjectId : string : 专题主键
                params: headers : 请求头
        """
        subjectId = self.get_value_choice(subjectId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_subjectweb.content_subjectweb_del(**_kwargs)

        self.assert_content_subjectweb_del(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="专题-后台官网查询专题详情-Y")
    def content_subjectweb_detail(self, subjectId="$None$", _assert=True,  **kwargs):
        """
            url=/content/subjectweb/detail
                params: subjectId :  :
                params: headers : 请求头
        """
        subjectId = self.get_list_choice(subjectId, list_or_dict=None, key="subjectId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_subjectweb.content_subjectweb_detail(**_kwargs)

        self.assert_content_subjectweb_detail(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="新闻中心文章列表-Y")
    def content_subjectweb_detailessaynew(self, current=1, subjectId="$None$", size=10, _assert=True,  **kwargs):
        """
            url=/content/subjectweb/detailEssayNew
                params: current :  :
                params: size :  :
                params: subjectId :  : 2 官方新闻 3 自媒体 4 媒体报道  null 全部
                params: headers : 请求头
        """
        subjectId = self.get_list_choice(subjectId, list_or_dict=None, key="subjectId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_subjectweb.content_subjectweb_detailessaynew(**_kwargs)

        self.assert_content_subjectweb_detailessaynew(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


