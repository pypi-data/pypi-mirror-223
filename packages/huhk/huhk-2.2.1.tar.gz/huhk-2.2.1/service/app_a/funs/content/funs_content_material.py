import allure

from service.app_a.asserts.content.asserts_content_material import AssertsContentMaterial
from service.app_a.apis.content import apis_content_material
from service.app_a.funs.content.material.funs_content_material_getmateriallist import FunsContentMaterialGetmateriallist


class FunsContentMaterial(AssertsContentMaterial, FunsContentMaterialGetmateriallist):
    @allure.step(title="素材-删除分组-Y")
    def content_material_delgroup(self, groupId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/material/delGroup
                params: groupId : number : 素材分组主键
                params: headers : 请求头
        """
        groupId = self.get_value_choice(groupId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_material.content_material_delgroup(**_kwargs)

        self.assert_content_material_delgroup(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="素材-批量删除")
    def content_material_delmaterial(self, _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/material/delMaterial
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_material.content_material_delmaterial(**_kwargs)

        self.assert_content_material_delmaterial(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="素材-更新素材分组-Y")
    def content_material_updategroup(self, groupName="$None$", groupId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/material/updateGroup
                params: groupName : string : 分组名称
                params: groupId : number : 分组主键
                params: headers : 请求头
        """
        groupName = self.get_value_choice(groupName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        groupId = self.get_value_choice(groupId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_material.content_material_updategroup(**_kwargs)

        self.assert_content_material_updategroup(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="素材-根据素材组获取素材列表")
    def content_material_getmateriallist(self, current=1, groupId="$None$", size=10, _assert=True,  **kwargs):
        """
            url=/content/material/getMaterialList
                params: groupId :  : 分组主键
                params: size :  : 每页数据数
                params: current :  : 当前页
                params: headers : 请求头
        """
        groupId = self.get_list_choice(groupId, list_or_dict=None, key="groupId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_material.content_material_getmateriallist(**_kwargs)

        self.assert_content_material_getmateriallist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="素材-添加素材分组-Y")
    def content_material_addgroup(self, groupName="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/material/addGroup
                params: groupName : string : 分组名称
                params: headers : 请求头
        """
        groupName = self.get_value_choice(groupName, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_material.content_material_addgroup(**_kwargs)

        self.assert_content_material_addgroup(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="素材-素材上传")
    def content_material_addmaterial(self, file="$None$", groupId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/material/addMaterial
                params: file : file : 上传文件
                params: groupId : text : 所属分组主键
                params: headers : 请求头
        """
        file = self.get_value_choice(file, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        groupId = self.get_value_choice(groupId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_material.content_material_addmaterial(**_kwargs)

        self.assert_content_material_addmaterial(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="素材-素材组列表-Y")
    def content_material_getgrouplist(self, groupName="$None$", _assert=True,  **kwargs):
        """
            url=/content/material/getGroupList
                params: groupName :  :
                params: headers : 请求头
        """
        groupName = self.get_list_choice(groupName, list_or_dict=None, key="groupName")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_material.content_material_getgrouplist(**_kwargs)

        self.assert_content_material_getgrouplist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


