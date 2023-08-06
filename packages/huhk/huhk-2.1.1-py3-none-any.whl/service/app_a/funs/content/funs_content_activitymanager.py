import allure

from service.app_a.asserts.content.asserts_content_activitymanager import AssertsContentActivitymanager
from service.app_a.apis.content import apis_content_activitymanager


class FunsContentActivitymanager(AssertsContentActivitymanager):
    @allure.step(title="活动 -修改报名人数(930)-Y")
    def content_activitymanager_updateperson(self, needLimitPeople="$None$", activityId="$None$", limitPeople="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/activityManager/updatePerson
                params: activityId : string : 活动Id
                params: needLimitPeople : string : 是否限制 0 不限制 1限制
                params: limitPeople : number : 限制人数
                params: headers : 请求头
        """
        needLimitPeople = self.get_value_choice(needLimitPeople, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        activityId = self.get_value_choice(activityId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        limitPeople = self.get_value_choice(limitPeople, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_activitymanager.content_activitymanager_updateperson(**_kwargs)

        self.assert_content_activitymanager_updateperson(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="活动 -修改报名时间-Y")
    def content_activitymanager_updateenrolltime(self, activityId="$None$", enrollStartTime="$None$", enrollTime="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/activityManager/updateEnrollTime
                params: activityId : string : 活动Id
                params: enrollStartTime : string : 报名开始时间
                params: enrollTime : string : 报名结束时间
                params: headers : 请求头
        """
        activityId = self.get_value_choice(activityId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        enrollStartTime = self.get_value_choice(enrollStartTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        enrollTime = self.get_value_choice(enrollTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_activitymanager.content_activitymanager_updateenrolltime(**_kwargs)

        self.assert_content_activitymanager_updateenrolltime(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="活动列表查询（930版本）-Y")
    def content_activitymanager_page(self, activityTimeSort="$None$", title="$None$", pushTimeSort="$None$", beginTime="$None$", status="$None$", province="$None$", createTimeSort="$None$", city="$None$", target="$None$", endTime="$None$", activityId="$None$", _assert=True,  **kwargs):
        """
            url=/content/activityManager/page
                params: activityId :  :
                params: title :  :
                params: beginTime :  : 2022-01-18 00:00:00 （一定要带上00:00:00）
                params: endTime :  : 2022-01-18 23:59:59 （一定要带上23:59:59）
                params: target :  : 1：全部用户,2：车主用户,3：非车主用户,4:使用人,5：车主&使用人,6：非车主&非使用人
                params: status :  : 活动状态: 不传查全部， 2.待审核  4.待发布 5.已发布 6.审核不过 7.已撤回 8.已归档 9.停止报名 10.已结束 11.已下架  ；查询时候传的状态：12.已删除
                params: province :  : 省（编码 areaId）全国则不需要传值
                params: city :  : 市（编码areaId）
                params: createTimeSort :  : 创建时间排序（DESC（倒序））|ASC（正序））
                params: activityTimeSort :  : 活动时间排序（DESC|ASC）
                params: pushTimeSort :  : 发布时间排序（DESC|ASC）
                params: headers : 请求头
        """
        activityTimeSort = self.get_list_choice(activityTimeSort, list_or_dict=None, key="activityTimeSort")
        title = self.get_list_choice(title, list_or_dict=None, key="title")
        pushTimeSort = self.get_list_choice(pushTimeSort, list_or_dict=None, key="pushTimeSort")
        beginTime = self.get_list_choice(beginTime, list_or_dict=None, key="beginTime")
        status = self.get_list_choice(status, list_or_dict=None, key="status")
        province = self.get_list_choice(province, list_or_dict=None, key="province")
        createTimeSort = self.get_list_choice(createTimeSort, list_or_dict=None, key="createTimeSort")
        city = self.get_list_choice(city, list_or_dict=None, key="city")
        target = self.get_list_choice(target, list_or_dict=None, key="target")
        endTime = self.get_list_choice(endTime, list_or_dict=None, key="endTime")
        activityId = self.get_list_choice(activityId, list_or_dict=None, key="activityId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_activitymanager.content_activitymanager_page(**_kwargs)

        self.assert_content_activitymanager_page(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="活动操作停止报名和结束活动-Y")
    def content_activitymanager_actinfoupdate(self, operationType="$None$", activityId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/activityManager/actInfoUpdate
                params: activityId : text : 活动ID
                params: operationType : text : 1停止报名 2活动结束
                params: headers : 请求头
        """
        operationType = self.get_value_choice(operationType, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        activityId = self.get_value_choice(activityId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_activitymanager.content_activitymanager_actinfoupdate(**_kwargs)

        self.assert_content_activitymanager_actinfoupdate(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="设置活动权重(930版本)-Y")
    def content_activitymanager_setactivitysort(self, activityId="$None$", sort="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/activityManager/setActivitySort
                params: activityId : string : 活动Id
                params: sort : number : 权重
                params: headers : 请求头
        """
        activityId = self.get_value_choice(activityId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        sort = self.get_value_choice(sort, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_activitymanager.content_activitymanager_setactivitysort(**_kwargs)

        self.assert_content_activitymanager_setactivitysort(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="获取活动详情-Y")
    def content_activitymanager_getactivityinfo_(self, activityId="$None$", _assert=True,  **kwargs):
        """
            url=/content/activityManager/getActivityInfo/{activityId}
                params: activityId :  :
                params: headers : 请求头
        """
        activityId = self.get_list_choice(activityId, list_or_dict=None, key="activityId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_activitymanager.content_activitymanager_getactivityinfo_(**_kwargs)

        self.assert_content_activitymanager_getactivityinfo_(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="活动置顶/取消置顶-Y")
    def content_activitymanager_activitytop_(self, activityId="$None$", topFlag="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/activityManager/activityTop/
                params: activityId : text : 活动ID
                params: topFlag : text : 0不置顶  1置顶
                params: headers : 请求头
        """
        activityId = self.get_value_choice(activityId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        topFlag = self.get_value_choice(topFlag, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_activitymanager.content_activitymanager_activitytop_(**_kwargs)

        self.assert_content_activitymanager_activitytop_(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="活动报名用户数据导出-Y")
    def content_activitymanager_activityjoinuserexport(self, activityId="$None$", _assert=True,  **kwargs):
        """
            url=/content/activityManager/activityJoinUserExport
                params: activityId :  : 活动Id
                params: headers : 请求头
        """
        activityId = self.get_list_choice(activityId, list_or_dict=None, key="activityId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_activitymanager.content_activitymanager_activityjoinuserexport(**_kwargs)

        self.assert_content_activitymanager_activityjoinuserexport(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="活动新增-Y")
    def content_activitymanager_save(self, title="$None$", publishType="$None$", authId="$None$", coordinate="$None$", county="$None$", activityPicUrl="$None$", status="$None$", province="$None$", publishTime="$None$", needLimitPeople="$None$", content="$None$", reason="$None$", activityId="$None$", enrollTime="$None$", activityAddr="$None$", city="$None$", agreementId="$None$", activityPicURL="$None$", needArea="$None$", beginTime="$None$", customerGroup="$None$", endTime="$None$", enrollStartTime="$None$", limitPeople="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/activityManager/save
                params: activityId : text :
                params: title : text :
                params: reason : text :
                params: activityPicUrl : text :
                params: beginTime : text :
                params: endTime : text : 汉字
                params: needArea : text : 汉字
                params: province : text : 汉字
                params: city : text : 34.232342,112.342345
                params: county : text :
                params: coordinate : text :
                params: needLimitPeople : text :
                params: limitPeople : text :
                params: enrollStartTime : text :
                params: enrollTime : text :
                params: publishType : text : 地图获取
                params: publishTime : text :
                params: content : text :
                params: authId : text :
                params: status : text :
                params: activityAddr : text :
                params: customerGroup : text :
                params: activityPicURL : string : 活动封面图
                params: agreementId : number : 协议ID
                params: headers : 请求头
        """
        title = self.get_value_choice(title, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        publishType = self.get_value_choice(publishType, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        authId = self.get_value_choice(authId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        coordinate = self.get_value_choice(coordinate, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        county = self.get_value_choice(county, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        activityPicUrl = self.get_value_choice(activityPicUrl, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        status = self.get_value_choice(status, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        province = self.get_value_choice(province, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        publishTime = self.get_value_choice(publishTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        needLimitPeople = self.get_value_choice(needLimitPeople, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        content = self.get_value_choice(content, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        reason = self.get_value_choice(reason, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        activityId = self.get_value_choice(activityId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        enrollTime = self.get_value_choice(enrollTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        activityAddr = self.get_value_choice(activityAddr, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        city = self.get_value_choice(city, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        agreementId = self.get_value_choice(agreementId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        activityPicURL = self.get_value_choice(activityPicURL, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        needArea = self.get_value_choice(needArea, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        beginTime = self.get_value_choice(beginTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        customerGroup = self.get_value_choice(customerGroup, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        endTime = self.get_value_choice(endTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        enrollStartTime = self.get_value_choice(enrollStartTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        limitPeople = self.get_value_choice(limitPeople, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_activitymanager.content_activitymanager_save(**_kwargs)

        self.assert_content_activitymanager_save(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="活动编辑（930版本）-Y")
    def content_activitymanager_update(self, title="$None$", publishType="$None$", authId="$None$", coordinate="$None$", county="$None$", activityPicUrl="$None$", status="$None$", province="$None$", publishTime="$None$", content="$None$", needLimitPeople="$None$", reason="$None$", activityId="$None$", enrollTime="$None$", activityAddr="$None$", city="$None$", activityPicURL="$None$", needArea="$None$", beginTime="$None$", customerGroup="$None$", endTime="$None$", enrollStartTime="$None$", limitPeople="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/activityManager/update
                params: activityId : text :
                params: title : text :
                params: reason : text :
                params: activityPicUrl : text :
                params: beginTime : text :
                params: endTime : text :
                params: province : text : 汉字
                params: city : text : 汉字
                params: county : text :
                params: coordinate : text : 34.232342,112.342345
                params: limitPeople : text :
                params: enrollTime : text :
                params: publishType : text :
                params: publishTime : text :
                params: content : text :
                params: authId : text :
                params: activityPicURL : string : 活动封面图
                params: needArea : string : 是否需要区域
                params: needLimitPeople : string : 是否需要人数限制
                params: enrollStartTime : string : 报名开始时间
                params: status : integer : 活动状态: 不传查全部
                * 2:待审核
                * 3:审核通过
                * 4:待上架
                * 5:已上架
                * 6:审核不通过
                * 9:停止报名
                * 10:已结束
                * 11:已下架
                * 12:已删除
                params: activityAddr : string : 活动地址
                params: customerGroup : string : 参与对象（1：全部用户，2：车主用户，3：非车主用户）
                params: headers : 请求头
        """
        title = self.get_value_choice(title, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        publishType = self.get_value_choice(publishType, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        authId = self.get_value_choice(authId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        coordinate = self.get_value_choice(coordinate, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        county = self.get_value_choice(county, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        activityPicUrl = self.get_value_choice(activityPicUrl, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        status = self.get_value_choice(status, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        province = self.get_value_choice(province, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        publishTime = self.get_value_choice(publishTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        content = self.get_value_choice(content, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        needLimitPeople = self.get_value_choice(needLimitPeople, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        reason = self.get_value_choice(reason, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        activityId = self.get_value_choice(activityId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        enrollTime = self.get_value_choice(enrollTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        activityAddr = self.get_value_choice(activityAddr, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        city = self.get_value_choice(city, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        activityPicURL = self.get_value_choice(activityPicURL, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        needArea = self.get_value_choice(needArea, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        beginTime = self.get_value_choice(beginTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        customerGroup = self.get_value_choice(customerGroup, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        endTime = self.get_value_choice(endTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        enrollStartTime = self.get_value_choice(enrollStartTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        limitPeople = self.get_value_choice(limitPeople, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_activitymanager.content_activitymanager_update(**_kwargs)

        self.assert_content_activitymanager_update(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="活动发布状态修改(930)-Y")
    def content_activitymanager_publishupdate(self, activityId="$None$", activityIds="$None$", publishStatus="$None$", status="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/activityManager/publishUpdate
                params: activityIds : text : 单个记录修改传["xxxxx"]
                params: publishStatus : text :
                params: activityId : string : 活动Id
                params: status : number : //状态: 1.新建 2.待审核 3.审核通过 4.待发布 5.已发布 6.审核不过 7.已撤回 8.已归档 9.停止报名 10.已结束 11.已下架；查询时候传的状态：12.已删除
                params: headers : 请求头
        """
        activityId = self.get_value_choice(activityId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        activityIds = self.get_value_choice(activityIds, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        publishStatus = self.get_value_choice(publishStatus, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        status = self.get_value_choice(status, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_activitymanager.content_activitymanager_publishupdate(**_kwargs)

        self.assert_content_activitymanager_publishupdate(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="活动审核状态修改-Y")
    def content_activitymanager_statusupdate(self, checkStatus="$None$", activityIds="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/activityManager/statusUpdate
                params: checkStatus : text :
                params: activityIds : array : 活动IDs
                type : string : None
                params: headers : 请求头
        """
        checkStatus = self.get_value_choice(checkStatus, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        activityIds = self.get_value_choice(activityIds, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_activitymanager.content_activitymanager_statusupdate(**_kwargs)

        self.assert_content_activitymanager_statusupdate(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="活动报名状态修改-Y")
    def content_activitymanager_enrollupdate(self, checkEnroll="$None$", activityIds="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/activityManager/enrollUpdate
                params: activityIds : text : 单个记录修改传["xxxxx"]
                params: checkEnroll : text :
                params: headers : 请求头
        """
        checkEnroll = self.get_value_choice(checkEnroll, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        activityIds = self.get_value_choice(activityIds, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_activitymanager.content_activitymanager_enrollupdate(**_kwargs)

        self.assert_content_activitymanager_enrollupdate(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="活动数据导出-Y")
    def content_activitymanager_activityexport(self, activityTimeSort="$None$", title="$None$", pushTimeSort="$None$", beginTime="$None$", status="$None$", province="$None$", createTimeSort="$None$", city="$None$", target="$None$", endTime="$None$", activityId="$None$", _assert=True,  **kwargs):
        """
            url=/content/activityManager/activityExport
                params: activityId :  :
                params: title :  :
                params: beginTime :  : 2022-01-18 00:00:00 （一定要带上00:00:00）
                params: endTime :  : 2022-01-18 23:59:59 （一定要带上23:59:59）
                params: target :  : 1：全部用户,2：车主用户,3：非车主用户,4:使用人,5：车主&使用人,6：非车主&非使用人
                params: status :  : 活动状态: 不传查全部， 2.待审核  4.待发布 5.已发布 6.审核不过 7.已撤回 8.已归档 9.停止报名 10.已结束 11.已下架  ；查询时候传的状态：12.已删除
                params: province :  : 省（编码 areaId）全国则不需要传值
                params: city :  : 市（编码areaId）
                params: createTimeSort :  : 创建时间排序（DESC（倒序））|ASC（正序））
                params: activityTimeSort :  : 活动时间排序（DESC|ASC）
                params: pushTimeSort :  : 发布时间排序（DESC|ASC）
                params: headers : 请求头
        """
        activityTimeSort = self.get_list_choice(activityTimeSort, list_or_dict=None, key="activityTimeSort")
        title = self.get_list_choice(title, list_or_dict=None, key="title")
        pushTimeSort = self.get_list_choice(pushTimeSort, list_or_dict=None, key="pushTimeSort")
        beginTime = self.get_list_choice(beginTime, list_or_dict=None, key="beginTime")
        status = self.get_list_choice(status, list_or_dict=None, key="status")
        province = self.get_list_choice(province, list_or_dict=None, key="province")
        createTimeSort = self.get_list_choice(createTimeSort, list_or_dict=None, key="createTimeSort")
        city = self.get_list_choice(city, list_or_dict=None, key="city")
        target = self.get_list_choice(target, list_or_dict=None, key="target")
        endTime = self.get_list_choice(endTime, list_or_dict=None, key="endTime")
        activityId = self.get_list_choice(activityId, list_or_dict=None, key="activityId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_activitymanager.content_activitymanager_activityexport(**_kwargs)

        self.assert_content_activitymanager_activityexport(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="活动状态流程-Y")
    def content_activitymanager_listlog(self, activityId="$None$", _assert=True,  **kwargs):
        """
            url=/content/activityManager/listLog
                params: activityId :  : 活动id
                params: headers : 请求头
        """
        activityId = self.get_list_choice(activityId, list_or_dict=None, key="activityId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_activitymanager.content_activitymanager_listlog(**_kwargs)

        self.assert_content_activitymanager_listlog(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


