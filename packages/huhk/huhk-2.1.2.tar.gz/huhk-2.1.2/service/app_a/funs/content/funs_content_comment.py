import allure

from service.app_a.asserts.content.asserts_content_comment import AssertsContentComment
from service.app_a.apis.content import apis_content_comment


class FunsContentComment(AssertsContentComment):
    @allure.step(title="评论-状态扭转（通用）-Y")
    def content_comment_updatestatus(self, commentId="$None$", fromStatus="$None$", toStatus="$None$", commentType="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/comment/updateStatus
                params: commentId :  : 评论主键
                params: commentType :  : 评论类型1：文章评论2：动态评论
                params: fromStatus :  : 当前状态
                params: toStatus :  : 扭转状态
                params: headers : 请求头
        """
        commentId = self.get_value_choice(commentId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        fromStatus = self.get_value_choice(fromStatus, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        toStatus = self.get_value_choice(toStatus, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        commentType = self.get_value_choice(commentType, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_comment.content_comment_updatestatus(**_kwargs)

        self.assert_content_comment_updatestatus(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="评论-评论导出-Y")
    def content_comment_download(self, downloadType="$None$", nickName="$None$", status="$None$", mobile="$None$", keyWord="$None$", contentCommentIds="$None$", startTime="$None$", endTime="$None$", EssayCommentIds="$None$", _assert=True,  **kwargs):
        """
            url=/content/comment/downLoad
                params: mobile :  : 评论用户手机号
                params: nickName :  : 评论昵称
                params: keyWord :  : 搜索关键字
                params: startTime :  : 搜索起始时间
                params: endTime :  : 搜索结束时间
                params: status :  : 状态0.待审核 1.已审核 2.审核未通过3：已发布4：已屏蔽
                params: downloadType :  : 1：根据搜索条件导出2：多选导出
                params: EssayCommentIds :  : 文章评论主键，用英文,隔开
                params: contentCommentIds :  : 动态评论主键，用英文,隔开
                params: headers : 请求头
        """
        downloadType = self.get_list_choice(downloadType, list_or_dict=None, key="downloadType")
        nickName = self.get_list_choice(nickName, list_or_dict=None, key="nickName")
        status = self.get_list_choice(status, list_or_dict=None, key="status")
        mobile = self.get_list_choice(mobile, list_or_dict=None, key="mobile")
        keyWord = self.get_list_choice(keyWord, list_or_dict=None, key="keyWord")
        contentCommentIds = self.get_list_choice(contentCommentIds, list_or_dict=None, key="contentCommentIds")
        startTime = self.get_list_choice(startTime, list_or_dict=None, key="startTime")
        endTime = self.get_list_choice(endTime, list_or_dict=None, key="endTime")
        EssayCommentIds = self.get_list_choice(EssayCommentIds, list_or_dict=None, key="EssayCommentIds")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_comment.content_comment_download(**_kwargs)

        self.assert_content_comment_download(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="评论-评论置顶（通用）-Y")
    def content_comment_commenttop(self, commentId="$None$", topFlag="$None$", commentType="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/comment/commentTop
                params: commentId : string : 评论主键
                params: commentType : number : 评论类型1：文章评论2：动态评论
                params: topFlag : number : 1：置顶0：取消置顶
                params: headers : 请求头
        """
        commentId = self.get_value_choice(commentId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        topFlag = self.get_value_choice(topFlag, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        commentType = self.get_value_choice(commentType, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_comment.content_comment_commenttop(**_kwargs)

        self.assert_content_comment_commenttop(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="后台管理-评论管理列表1030-Y")
    def content_comment_list(self, commentType="$None$", nickName="$None$", current=1, checkedStatus="$None$", mobile="$None$", keyWord="$None$", essayId="$None$", startTime="$None$", endTime="$None$", size=10, _assert=True,  **kwargs):
        """
            url=/content/comment/list
                params: nickName :  : 用户昵称 String
                params: keyWord :  : 搜索内容关键字  String
                params: startTime :  : 搜索开始时间 yyyy-MM-dd HH:mm:ss
                params: endTime :  : 搜索结束时间 yyyy-MM-dd HH:mm:ss
                params: size :  : 每页数量数
                params: current :  : 当前页
                params: commentType :  : 评论类型1：文章评论 2：动态 Integer
                params: checkedStatus :  : 审核状态 0待审核 1.已上架 2.审核未通过3：已发布 5已删除 Integer
                params: mobile :  : 电话 string
                params: essayId :  : 文章(资讯)主键 string
                params: headers : 请求头
        """
        commentType = self.get_list_choice(commentType, list_or_dict=None, key="commentType")
        nickName = self.get_list_choice(nickName, list_or_dict=None, key="nickName")
        checkedStatus = self.get_list_choice(checkedStatus, list_or_dict=None, key="checkedStatus")
        mobile = self.get_list_choice(mobile, list_or_dict=None, key="mobile")
        keyWord = self.get_list_choice(keyWord, list_or_dict=None, key="keyWord")
        essayId = self.get_list_choice(essayId, list_or_dict=None, key="essayId")
        startTime = self.get_list_choice(startTime, list_or_dict=None, key="startTime")
        endTime = self.get_list_choice(endTime, list_or_dict=None, key="endTime")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_comment.content_comment_list(**_kwargs)

        self.assert_content_comment_list(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="评论-屏蔽评论-Y")
    def content_comment_delete(self, commentId="$None$", toStatus="$None$", commentType="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/content/comment/delete
                params: commentId : string : 评论主键
                params: commentType : number : 1：文章评论2：动态评论
                params: toStatus : string :
                params: headers : 请求头
        """
        commentId = self.get_value_choice(commentId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        toStatus = self.get_value_choice(toStatus, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        commentType = self.get_value_choice(commentType, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content_comment.content_comment_delete(**_kwargs)

        self.assert_content_comment_delete(_assert, **_kwargs)
        self.set_value(_kwargs)


