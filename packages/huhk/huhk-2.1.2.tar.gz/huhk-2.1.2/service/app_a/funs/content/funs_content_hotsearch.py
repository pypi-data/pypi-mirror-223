import allure

from service.app_a.asserts.content.asserts_content_hotsearch import AssertsContentHotsearch
from service.app_a.apis.content import apis_content_hotsearch


class FunsContentHotsearch(AssertsContentHotsearch):
    @allure.step(title="热门搜索-修改权重-Y")
    def content_hotsearch_rank(self, kId="$None$", rank="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/hotSearch/rank
                params: kId : string : 主键id
                params: rank : string : 权重
                params: headers : 请求头
        """
        kId = self.get_value_choice(kId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        rank = self.get_value_choice(rank, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_hotsearch.content_hotsearch_rank(**_kwargs)

        self.assert_content_hotsearch_rank(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="热门搜索-列表-Y")
    def content_hotsearch_list(self, kId="$None$", rank="$None$", _assert=True,  **kwargs):
        """
            url=/content/hotSearch/list
                params: kId : string : 主键id
                params: rank : string : 权重
                params: headers : 请求头
        """
        kId = self.get_list_choice(kId, list_or_dict=None, key="kId")
        rank = self.get_list_choice(rank, list_or_dict=None, key="rank")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_hotsearch.content_hotsearch_list(**_kwargs)

        self.assert_content_hotsearch_list(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="热门搜索-新增-Y")
    def content_hotsearch_insert(self, keyWord="$None$", point="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/hotSearch/insert
                params: keyWord : string : 关键词(城市名)
                params: point : string : 1 发现-搜索 4 活动定位
                params: headers : 请求头
        """
        keyWord = self.get_value_choice(keyWord, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        point = self.get_value_choice(point, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_hotsearch.content_hotsearch_insert(**_kwargs)

        self.assert_content_hotsearch_insert(_assert, **_kwargs)
        self.set_value(_kwargs)


