from service.app_a.funs.order.funs_order_rightsorder import FunsOrderRightsorder
from service.app_a.funs.order.funs_order_mainorder import FunsOrderMainorder
from service.app_a.funs.order.funs_order_order import FunsOrderOrder
from service.app_a.funs.order.funs_order_rights import FunsOrderRights
from service.app_a.funs.order.funs_order_testdrive import FunsOrderTestdrive
from service.app_a.funs.order.funs_order_freeorder import FunsOrderFreeorder


class FunsOrder(FunsOrderRightsorder, FunsOrderMainorder, FunsOrderOrder, FunsOrderRights, FunsOrderTestdrive, FunsOrderFreeorder):
    pass

