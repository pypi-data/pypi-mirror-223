import allure

from service.app_a.asserts.content.material.asserts_content_material_getmateriallist import AssertsContentMaterialGetmateriallist
from service.app_a.apis.content.material import apis_content_material_getmateriallist


class FunsContentMaterialGetmateriallist(AssertsContentMaterialGetmateriallist):
    @allure.step(title="素材-根据素材组获取素材列表_copy")
    def content_material_getmateriallist_1659319316474(self, current=1, groupId="$None$", size=10, _assert=True,  **kwargs):
        """
            url=/content/material/getMaterialList_1659319316474
                params: groupId :  : 分组主键
                params: size :  : 每页数据数
                params: current :  : 当前页
                params: headers : 请求头
        """
        groupId = self.get_list_choice(groupId, list_or_dict=None, key="groupId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_material_getmateriallist.content_material_getmateriallist_1659319316474(**_kwargs)

        self.assert_content_material_getmateriallist_1659319316474(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


