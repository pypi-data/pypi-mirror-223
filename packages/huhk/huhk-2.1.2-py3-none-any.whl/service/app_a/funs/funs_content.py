from service.app_a.apis import apis_content
from service.app_a.asserts.asserts_content import AssertsContent
import allure
from service.app_a.funs.content.funs_content_campmanager import FunsContentCampmanager
from service.app_a.funs.content.funs_content_activitymanager import FunsContentActivitymanager
from service.app_a.funs.content.funs_content_messagemanager import FunsContentMessagemanager
from service.app_a.funs.content.funs_content_noticemanager import FunsContentNoticemanager
from service.app_a.funs.content.funs_content_adv import FunsContentAdv
from service.app_a.funs.content.funs_content_agreement import FunsContentAgreement
from service.app_a.funs.content.funs_content_essay import FunsContentEssay
from service.app_a.funs.content.funs_content_subject import FunsContentSubject
from service.app_a.funs.content.funs_content_subjectweb import FunsContentSubjectweb
from service.app_a.funs.content.funs_content_essayweb import FunsContentEssayweb
from service.app_a.funs.content.funs_content_contentmanager import FunsContentContentmanager
from service.app_a.funs.content.funs_content_essaycomment import FunsContentEssaycomment
from service.app_a.funs.content.funs_content_commonquestion import FunsContentCommonquestion
from service.app_a.funs.content.funs_content_recruit import FunsContentRecruit
from service.app_a.funs.content.funs_content_advplace import FunsContentAdvplace
from service.app_a.funs.content.funs_content_hotcity import FunsContentHotcity
from service.app_a.funs.content.funs_content_hotsearch import FunsContentHotsearch
from service.app_a.funs.content.funs_content_material import FunsContentMaterial
from service.app_a.funs.content.funs_content_comment import FunsContentComment
from service.app_a.funs.content.funs_content_topic4c import FunsContentTopic4C
from service.app_a.funs.content.funs_content_question import FunsContentQuestion
from service.app_a.funs.content.funs_content_safecode import FunsContentSafecode


class FunsContent(FunsContentCampmanager, FunsContentActivitymanager, FunsContentMessagemanager, FunsContentNoticemanager, FunsContentAdv, AssertsContent, FunsContentAgreement, FunsContentEssay, FunsContentSubject, FunsContentSubjectweb, FunsContentEssayweb, FunsContentContentmanager, FunsContentEssaycomment, FunsContentCommonquestion, FunsContentRecruit, FunsContentAdvplace, FunsContentHotcity, FunsContentHotsearch, FunsContentMaterial, FunsContentComment, FunsContentTopic4C, FunsContentQuestion, FunsContentSafecode):
    @allure.step(title="点位内容-通过id删除点位内容-Y")
    def content_adv_(self, advId="$None$", _assert=True,  **kwargs):
        """
            url=/content/adv/{advId}
                params: advId :  :
                params: headers : 请求头
        """
        advId = self.get_value_choice(advId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_content.content_adv_(**_kwargs)

        self.assert_content_adv_(_assert, **_kwargs)
        self.set_value(_kwargs)


