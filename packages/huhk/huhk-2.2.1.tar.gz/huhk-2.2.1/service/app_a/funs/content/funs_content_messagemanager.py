import allure

from service.app_a.asserts.content.asserts_content_messagemanager import AssertsContentMessagemanager
from service.app_a.apis.content import apis_content_messagemanager


class FunsContentMessagemanager(AssertsContentMessagemanager):
    @allure.step(title="消息列表查询接口-Y")
    def content_messagemanager_page(self, content="$None$", userId="$None$", authId="$None$", pEndTime="$None$", messageId="$None$", cStartTime="$None$", cEndTime="$None$", beginTime="$None$", status="$None$", pStartTime="$None$", endTime="$None$", _assert=True,  **kwargs):
        """
            url=/content/messageManager/page
                params: messageId :  :
                params: content :  :
                params: beginTime :  : 前端日期后面必须要追加 00:00:00
                params: endTime :  : 前端日期后面必须要追加 23:59:59
                params: authId :  :
                params: status :  : -1.结束 0.待审核 1.审核通过 2.审核未通过 3.草稿  4.未发布 5.已发布 6.已撤销 7.已归档
                params: pStartTime :  :
                params: pEndTime :  :
                params: cStartTime :  :
                params: cEndTime :  :
                params: headers : 请求头
        """
        content = self.get_list_choice(content, list_or_dict=None, key="content")
        userId = self.get_list_choice(userId, list_or_dict=None, key="userId")
        authId = self.get_list_choice(authId, list_or_dict=None, key="authId")
        pEndTime = self.get_list_choice(pEndTime, list_or_dict=None, key="pEndTime")
        messageId = self.get_list_choice(messageId, list_or_dict=None, key="messageId")
        cStartTime = self.get_list_choice(cStartTime, list_or_dict=None, key="cStartTime")
        cEndTime = self.get_list_choice(cEndTime, list_or_dict=None, key="cEndTime")
        beginTime = self.get_list_choice(beginTime, list_or_dict=None, key="beginTime")
        status = self.get_list_choice(status, list_or_dict=None, key="status")
        pStartTime = self.get_list_choice(pStartTime, list_or_dict=None, key="pStartTime")
        endTime = self.get_list_choice(endTime, list_or_dict=None, key="endTime")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_messagemanager.content_messagemanager_page(**_kwargs)

        self.assert_content_messagemanager_page(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="获取消息详情-Y")
    def content_messagemanager_getmessageinfo_(self, messageId="$None$", _assert=True,  **kwargs):
        """
            url=/content/messageManager/getMessageInfo/{messageId}
                params: messageId :  :
                params: headers : 请求头
        """
        messageId = self.get_list_choice(messageId, list_or_dict=None, key="messageId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_messagemanager.content_messagemanager_getmessageinfo_(**_kwargs)

        self.assert_content_messagemanager_getmessageinfo_(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="消息置顶/取消置顶-Y")
    def content_messagemanager_messagetop(self, messageIds="$None$", topFlag="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/messageManager/messageTop
                params: messageIds : text : 消息ids集合
                params: topFlag : text : 消息置顶标识 0-置顶 1-不置顶
                params: headers : 请求头
        """
        messageIds = self.get_value_choice(messageIds, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        topFlag = self.get_value_choice(topFlag, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_messagemanager.content_messagemanager_messagetop(**_kwargs)

        self.assert_content_messagemanager_messagetop(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="消息新增接口-Y")
    def content_messagemanager_insert(self, content="$None$", checkStatus="$None$", publishType="$None$", messageId="$None$", checkPublish="$None$", publishTime="$None$", param="$None$", sendScope="$None$", imageUrl="$None$", type="$None$", sourceType="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/messageManager/insert
                params: messageId : text :
                params: type : text : 此处传1
                params: content : text :
                params: imageUrl : text :
                params: sourceType : text : 此处传1
                params: param : text :
                params: sendScope : text :
                params: checkStatus : text :
                params: checkPublish : text :
                params: publishType : text :
                params: publishTime : text :
                params: headers : 请求头
        """
        content = self.get_value_choice(content, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        checkStatus = self.get_value_choice(checkStatus, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        publishType = self.get_value_choice(publishType, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        messageId = self.get_value_choice(messageId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        checkPublish = self.get_value_choice(checkPublish, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        publishTime = self.get_value_choice(publishTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        param = self.get_value_choice(param, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        sendScope = self.get_value_choice(sendScope, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        imageUrl = self.get_value_choice(imageUrl, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        type = self.get_value_choice(type, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        sourceType = self.get_value_choice(sourceType, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_messagemanager.content_messagemanager_insert(**_kwargs)

        self.assert_content_messagemanager_insert(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="消息编辑接口-Y")
    def content_messagemanager_update(self, content="$None$", checkStatus="$None$", messageId="$None$", checkPublish="$None$", userMobiles="$None$", param="$None$", sendScope="$None$", imageUrl="$None$", type="$None$", sourceType="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/messageManager/update
                params: messageId :  :
                params: type :  : 此处传1
                params: content :  :
                params: imageUrl :  :
                params: sourceType :  : 此处传1
                params: param :  :
                params: sendScope :  :
                params: checkStatus :  :
                params: checkPublish :  :
                params: userMobiles :  : ["131xxxx1234","132xxxx1234"]
                params: headers : 请求头
        """
        content = self.get_value_choice(content, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        checkStatus = self.get_value_choice(checkStatus, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        messageId = self.get_value_choice(messageId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        checkPublish = self.get_value_choice(checkPublish, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        userMobiles = self.get_value_choice(userMobiles, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        param = self.get_value_choice(param, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        sendScope = self.get_value_choice(sendScope, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        imageUrl = self.get_value_choice(imageUrl, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        type = self.get_value_choice(type, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        sourceType = self.get_value_choice(sourceType, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_messagemanager.content_messagemanager_update(**_kwargs)

        self.assert_content_messagemanager_update(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="消息发布状态修改-Y")
    def content_messagemanager_publishupdate(self, messageIds="$None$", publishStatus="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/messageManager/publishUpdate
                params: messageIds : text :
                params: publishStatus : text :
                params: headers : 请求头
        """
        messageIds = self.get_value_choice(messageIds, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        publishStatus = self.get_value_choice(publishStatus, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_messagemanager.content_messagemanager_publishupdate(**_kwargs)

        self.assert_content_messagemanager_publishupdate(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="消息审核状态修改")
    def content_messagemanager_statusupdate(self, messageIds="$None$", checkStatus="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/messageManager/statusUpdate
                params: messageIds : text :
                params: checkStatus : text :
                params: headers : 请求头
        """
        messageIds = self.get_value_choice(messageIds, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        checkStatus = self.get_value_choice(checkStatus, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_messagemanager.content_messagemanager_statusupdate(**_kwargs)

        self.assert_content_messagemanager_statusupdate(_assert, **_kwargs)
        self.set_value(_kwargs)


