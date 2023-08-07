import allure

from service.app_a.asserts.content.asserts_content_question import AssertsContentQuestion
from service.app_a.apis.content import apis_content_question


class FunsContentQuestion(AssertsContentQuestion):
    @allure.step(title="问答-回复问题-Y")
    def content_question_answerquestion(self, questionId="$None$", author="$None$", answerContent="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/question/answerQuestion
                params: questionId : string : 问题主键
                params: answerContent : string : 回答内容
                params: author : number : 作者
                params: headers : 请求头
        """
        questionId = self.get_value_choice(questionId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        author = self.get_value_choice(author, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        answerContent = self.get_value_choice(answerContent, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_question.content_question_answerquestion(**_kwargs)

        self.assert_content_question_answerquestion(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="问答-回答撤回归档-Y")
    def content_question_revoke(self, questionId="$None$", operaType="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/question/revoke
                params: operaType : string : 操作类型3：撤回4：归档
                params: questionId : string : 回复主键
                params: headers : 请求头
        """
        questionId = self.get_value_choice(questionId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        operaType = self.get_value_choice(operaType, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_question.content_question_revoke(**_kwargs)

        self.assert_content_question_revoke(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="问答-搜索问题列表-Y")
    def content_question_getmanegequestionlist(self, current=1, status="$None$", mobile="$None$", keyWord="$None$", startTime="$None$", endTime="$None$", size=10, _assert=True,  **kwargs):
        """
            url=/content/question/getManegeQuestionList
                params: keyWord :  : 关键字
                params: mobile :  : 发布人手机号
                params: startTime :  : 搜索起始时间
                params: endTime :  : 搜索结束时间
                params: status :  : 问答状态1：已回复、0：待回复、3：已撤回、4：已归档
                params: size :  : 每页数据量
                params: current :  : 页数
                params: headers : 请求头
        """
        status = self.get_list_choice(status, list_or_dict=None, key="status")
        mobile = self.get_list_choice(mobile, list_or_dict=None, key="mobile")
        keyWord = self.get_list_choice(keyWord, list_or_dict=None, key="keyWord")
        startTime = self.get_list_choice(startTime, list_or_dict=None, key="startTime")
        endTime = self.get_list_choice(endTime, list_or_dict=None, key="endTime")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_question.content_question_getmanegequestionlist(**_kwargs)

        self.assert_content_question_getmanegequestionlist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="问答-获取问题详情页面-Y")
    def content_question_getbyid(self, questionId="$None$", _assert=True,  **kwargs):
        """
            url=/content/question/getById
                params: questionId :  : 问题主键
                params: headers : 请求头
        """
        questionId = self.get_list_choice(questionId, list_or_dict=None, key="questionId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_question.content_question_getbyid(**_kwargs)

        self.assert_content_question_getbyid(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


