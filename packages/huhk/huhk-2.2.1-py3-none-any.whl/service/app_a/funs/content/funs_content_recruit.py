import allure

from service.app_a.asserts.content.asserts_content_recruit import AssertsContentRecruit
from service.app_a.apis.content import apis_content_recruit


class FunsContentRecruit(AssertsContentRecruit):
    @allure.step(title="招聘信息保存-Y")
    def content_recruit_save(self, fileName="$None$", fileUrl="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/recruit/save
                params: fileName : string : 文件名
                params: fileUrl : string : 文件url
                params: headers : 请求头
        """
        fileName = self.get_value_choice(fileName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        fileUrl = self.get_value_choice(fileUrl, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_recruit.content_recruit_save(**_kwargs)

        self.assert_content_recruit_save(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="招聘信息查询-Y")
    def content_recruit_detail(self, _assert=True,  **kwargs):
        """
            url=/content/recruit/detail
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_recruit.content_recruit_detail(**_kwargs)

        self.assert_content_recruit_detail(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


