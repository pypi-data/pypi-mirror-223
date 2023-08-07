import allure

from service.app_a.asserts.content.asserts_content_subject import AssertsContentSubject
from service.app_a.apis.content import apis_content_subject


class FunsContentSubject(AssertsContentSubject):
    @allure.step(title="专题-后台App专题文章列表-Y")
    def content_subject_detailessay(self, subjectName="$None$", current=1, subjectId="$None$", size=10, _assert=True,  **kwargs):
        """
            url=/content/subject/detailEssay
                params: current :  :
                params: size :  :
                params: subjectId :  : Long
                params: subjectName :  :  string
                params: headers : 请求头
        """
        subjectName = self.get_list_choice(subjectName, list_or_dict=None, key="subjectName")
        subjectId = self.get_list_choice(subjectId, list_or_dict=None, key="subjectId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_subject.content_subject_detailessay(**_kwargs)

        self.assert_content_subject_detailessay(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="专题-后台App专题新增-Y")
    def content_subject_add(self, subPicUrl="$None$", subjectName="$None$", parentId="$None$", explain="$None$", status="$None$", level="$None$", type="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/subject/add
                params: subjectName : string : 专题名称
                params: parentId : string : 父级专题主键
                params: level : number : 专题等级
                params: status : number : 是否可用1：是0：否
                params: explain : string : 说明
                params: type : number : 关联类型
                params: subPicUrl : string : 专题图片
                params: headers : 请求头
        """
        subPicUrl = self.get_value_choice(subPicUrl, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        subjectName = self.get_value_choice(subjectName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        parentId = self.get_value_choice(parentId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        explain = self.get_value_choice(explain, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        status = self.get_value_choice(status, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        level = self.get_value_choice(level, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        type = self.get_value_choice(type, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_subject.content_subject_add(**_kwargs)

        self.assert_content_subject_add(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="专题-后台App删除专题-Y")
    def content_subject_del(self, subjectId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/subject/del
                params: subjectId : text :
                params: headers : 请求头
        """
        subjectId = self.get_value_choice(subjectId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_subject.content_subject_del(**_kwargs)

        self.assert_content_subject_del(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="专题-后台App移动专题更新-Y")
    def content_subject_mobilesubject(self, serial="$None$", parentId="$None$", subjectId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/subject/mobileSubject
                params: subjectId : text : 移动的专题ID
                params: parentId : text : 移动到的一级专题ID
                params: serial : text : 排序
                params: headers : 请求头
        """
        serial = self.get_value_choice(serial, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        parentId = self.get_value_choice(parentId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        subjectId = self.get_value_choice(subjectId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_subject.content_subject_mobilesubject(**_kwargs)

        self.assert_content_subject_mobilesubject(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="文章-发布到下拉数据-Y")
    def content_subject_getessaysubjects(self, _assert=True,  **kwargs):
        """
            url=/content/subject/getEssaySubjects
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_subject.content_subject_getessaysubjects(**_kwargs)

        self.assert_content_subject_getessaysubjects(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="专题-后台App查询专题详情-Y")
    def content_subject_detail(self, subjectId="$None$", _assert=True,  **kwargs):
        """
            url=/content/subject/detail
                params: subjectId :  : 广告位主键
                params: headers : 请求头
        """
        subjectId = self.get_list_choice(subjectId, list_or_dict=None, key="subjectId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_subject.content_subject_detail(**_kwargs)

        self.assert_content_subject_detail(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="专题-后台APP专题类型列表-Y")
    def content_subject_treelist(self, _assert=True,  **kwargs):
        """
            url=/content/subject/treeList
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_subject.content_subject_treelist(**_kwargs)

        self.assert_content_subject_treelist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="专题-后台App保存/更新-Y")
    def content_subject_save(self, delFlag="$None$", isService="$None$", isSearch="$None$", subPicUrl="$None$", subjectName="$None$", explain="$None$", parentId="$None$", status="$None$", level="$None$", siftFlag="$None$", subjectId="$None$", type="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/subject/save
                params: subjectId : number :
                params: subjectName : string :
                params: level : number :
                params: delFlag : number :
                params: subPicUrl : string :
                params: explain : string :
                params: status : number :
                params: type : number :
                params: parentId : string : 父ID
                params: siftFlag : number : 是否精选 1是 0否
                params: isService : number : 是否设置客服入口 1是 0否
                params: isSearch : number : 是否配置搜索 0否 1是
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
        level = self.get_value_choice(level, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        siftFlag = self.get_value_choice(siftFlag, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        subjectId = self.get_value_choice(subjectId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        type = self.get_value_choice(type, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_subject.content_subject_save(**_kwargs)

        self.assert_content_subject_save(_assert, **_kwargs)
        self.set_value(_kwargs)


