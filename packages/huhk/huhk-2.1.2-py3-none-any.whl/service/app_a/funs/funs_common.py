from service.app_a.funs.common.funs_common_systemversion import FunsCommonSystemversion
from service.app_a.funs.common.funs_common_remoteinterfacelog import FunsCommonRemoteinterfacelog
from service.app_a.funs.common.funs_common_user4c import FunsCommonUser4C
from service.app_a.funs.common.funs_common_clue import FunsCommonClue
from service.app_a.funs.common.funs_common_user import FunsCommonUser
from service.app_a.funs.common.funs_common_common import FunsCommonCommon
from service.app_a.funs.common.funs_common_userpointsmanage import FunsCommonUserpointsmanage


class FunsCommon(FunsCommonSystemversion, FunsCommonRemoteinterfacelog, FunsCommonUser4C, FunsCommonClue, FunsCommonUser, FunsCommonCommon, FunsCommonUserpointsmanage):
    pass

