import allure

from service.app_a.asserts.asserts_essay import AssertsEssay
from service.app_a.apis import apis_essay


class FunsEssay(AssertsEssay):
    @allure.step(title="文章-批量操作-Y")
    def essay_batch(self, essayId="$None$", batchType="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/essay/batch
                params: essayId :  : 文章主键
                params: batchType :  : 1：归档2：撤回3：置顶4：取消置顶
                params: headers : 请求头
        """
        essayId = self.get_value_choice(essayId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        batchType = self.get_value_choice(batchType, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_essay.essay_batch(**_kwargs)

        self.assert_essay_batch(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="文章-获取列表状态数量-Y")
    def essay_querylistcount(self, author="$None$", status="$None$", essayId="$None$", keyWord="$None$", subjectId="$None$", startTime="$None$", endTime="$None$", _assert=True,  **kwargs):
        """
            url=/essay/queryListCount
                params: essayId :  : 文章主键
                params: keyWord :  : 搜索关键字
                params: author :  : 作者
                params: startTime :  : 搜索起始时间
                params: endTime :  : 搜索结束时间
                params: subjectId :  : 专题主键
                params: status :  : 状态
                params: headers : 请求头
        """
        author = self.get_list_choice(author, list_or_dict=None, key="author")
        status = self.get_list_choice(status, list_or_dict=None, key="status")
        essayId = self.get_list_choice(essayId, list_or_dict=None, key="essayId")
        keyWord = self.get_list_choice(keyWord, list_or_dict=None, key="keyWord")
        subjectId = self.get_list_choice(subjectId, list_or_dict=None, key="subjectId")
        startTime = self.get_list_choice(startTime, list_or_dict=None, key="startTime")
        endTime = self.get_list_choice(endTime, list_or_dict=None, key="endTime")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_essay.essay_querylistcount(**_kwargs)

        self.assert_essay_querylistcount(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


