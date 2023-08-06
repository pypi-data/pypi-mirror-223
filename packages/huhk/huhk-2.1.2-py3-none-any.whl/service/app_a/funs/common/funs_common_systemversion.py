import allure

from service.app_a.asserts.common.asserts_common_systemversion import AssertsCommonSystemversion
from service.app_a.apis.common import apis_common_systemversion


class FunsCommonSystemversion(AssertsCommonSystemversion):
    @allure.step(title="保存版本信息-Y")
    def common_systemversion_save(self, remark="$None$", content="$None$", downloadUrl="$None$", force="$None$", size=10, publishStatus="$None$", version="$None$", versionId="$None$", classify="$None$", name="$None$", _assert=True,  **kwargs):
        """
            url=/common/systemversion/save
                params: version : string : 版本号
                params: name : string : 版本名称
                params: content : string : 更新内容
                params: remark : string : 备注
                params: classify : string :  Android或IOS
                params: force : string : 强制更新0.否1.是
                params: downloadUrl : string : 下载路径
                params: size : string : 大小
                params: versionId : number : 主键，更新传，新增不传
                params: publishStatus : number : 0. 未发布 1.已发布
                params: headers : 请求头
        """
        remark = self.get_list_choice(remark, list_or_dict=None, key="remark")
        content = self.get_list_choice(content, list_or_dict=None, key="content")
        downloadUrl = self.get_list_choice(downloadUrl, list_or_dict=None, key="downloadUrl")
        force = self.get_list_choice(force, list_or_dict=None, key="force")
        publishStatus = self.get_list_choice(publishStatus, list_or_dict=None, key="publishStatus")
        version = self.get_list_choice(version, list_or_dict=None, key="version")
        versionId = self.get_list_choice(versionId, list_or_dict=None, key="versionId")
        classify = self.get_list_choice(classify, list_or_dict=None, key="classify")
        name = self.get_list_choice(name, list_or_dict=None, key="name")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_common_systemversion.common_systemversion_save(**_kwargs)

        self.assert_common_systemversion_save(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="查询版本信息-Y")
    def common_systemversion_page(self, _assert=True,  **kwargs):
        """
            url=/common/systemversion/page
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_common_systemversion.common_systemversion_page(**_kwargs)

        self.assert_common_systemversion_page(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


