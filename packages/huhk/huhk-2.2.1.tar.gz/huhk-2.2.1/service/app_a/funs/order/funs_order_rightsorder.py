import allure

from service.app_a.asserts.order.asserts_order_rightsorder import AssertsOrderRightsorder
from service.app_a.apis.order import apis_order_rightsorder
from service.app_a.funs.order.rightsorder.funs_order_rightsorder_receive import FunsOrderRightsorderReceive


class FunsOrderRightsorder(AssertsOrderRightsorder, FunsOrderRightsorderReceive):
    @allure.step(title="权益订单导出接口-Y")
    def order_rightsorder_export(self, payDateBegin="$None$", userId="$None$", orderMainId="$None$", payDateEnd="$None$", receiveDateBegin="$None$", receiveDateEnd="$None$", useStatus="$None$", rightsType="$None$", mobile="$None$", rightsOrderId="$None$", _assert=True,  **kwargs):
        """
            url=/order/rightsOrder/export
                params: mobile :  : 手机号码
                params: rightsOrderId :  : 权益订单ID
                params: orderMainId :  : 主订单ID
                params: useStatus :  : 权益使用状态
                params: rightsType :  : 权益类型
                params: receiveDateBegin :  : 权益领取时间 - 开始
                params: receiveDateEnd :  : 权益领取时间 - 结束
                params: payDateBegin :  : 权益支付时间 - 开始
                params: payDateEnd :  : 权益支付时间 - 结束
                params: headers : 请求头
        """
        payDateBegin = self.get_list_choice(payDateBegin, list_or_dict=None, key="payDateBegin")
        userId = self.get_list_choice(userId, list_or_dict=None, key="userId")
        orderMainId = self.get_list_choice(orderMainId, list_or_dict=None, key="orderMainId")
        payDateEnd = self.get_list_choice(payDateEnd, list_or_dict=None, key="payDateEnd")
        receiveDateBegin = self.get_list_choice(receiveDateBegin, list_or_dict=None, key="receiveDateBegin")
        receiveDateEnd = self.get_list_choice(receiveDateEnd, list_or_dict=None, key="receiveDateEnd")
        useStatus = self.get_list_choice(useStatus, list_or_dict=None, key="useStatus")
        rightsType = self.get_list_choice(rightsType, list_or_dict=None, key="rightsType")
        mobile = self.get_list_choice(mobile, list_or_dict=None, key="mobile")
        rightsOrderId = self.get_list_choice(rightsOrderId, list_or_dict=None, key="rightsOrderId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_rightsorder.order_rightsorder_export(**_kwargs)

        self.assert_order_rightsorder_export(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="权益订单 - 新增-Y")
    def order_rightsorder_insert(self, orderMainId="$None$", userId="$None$", rightsId="$None$", createBy="$None$", payDate="$None$", createTime="$None$", refundDate="$None$", payBillNo="$None$", useStatus="$None$", rightsType="$None$", rightsName="$None$", payAmount="$None$", mobile="$None$", receiveDate="$None$", refundBillNo="$None$", updateId="$None$", updateTime="$None$", rightsOrderId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/order/rightsOrder/insert
                params: rightsOrderId : number : 权益订单ID
                params: rightsId : number : 权益ID
                params: rightsType : integer : 权益类型
                params: rightsName : string : 权益名称
                params: orderMainId : string : 主订单ID
                params: mobile : string : 用户手机号
                params: payAmount : string : 支付金额
                params: useStatus : integer : 权益使用状态
                params: receiveDate : string : 权益领取时间
                params: payDate : string : 权益支付时间
                params: refundDate : string : 权益退款时间
                params: payBillNo : string : 支付流水
                params: refundBillNo : string : 退款流水
                params: createTime : string : 创建时间
                params: createBy : number : 创建人
                params: updateTime : string : 更新时间
                params: updateId : number : 更新人id
                params: headers : 请求头
        """
        orderMainId = self.get_value_choice(orderMainId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        userId = self.get_value_choice(userId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        rightsId = self.get_value_choice(rightsId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        createBy = self.get_value_choice(createBy, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        payDate = self.get_value_choice(payDate, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        createTime = self.get_value_choice(createTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        refundDate = self.get_value_choice(refundDate, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        payBillNo = self.get_value_choice(payBillNo, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        useStatus = self.get_value_choice(useStatus, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        rightsType = self.get_value_choice(rightsType, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        rightsName = self.get_value_choice(rightsName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        payAmount = self.get_value_choice(payAmount, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        mobile = self.get_value_choice(mobile, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        receiveDate = self.get_value_choice(receiveDate, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        refundBillNo = self.get_value_choice(refundBillNo, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        updateId = self.get_value_choice(updateId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        updateTime = self.get_value_choice(updateTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        rightsOrderId = self.get_value_choice(rightsOrderId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_rightsorder.order_rightsorder_insert(**_kwargs)

        self.assert_order_rightsorder_insert(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="权益订单 - 分页查询-Y")
    def order_rightsorder_page(self, payDateBegin="$None$", userId="$None$", orderMainId="$None$", payDateEnd="$None$", receiveDateBegin="$None$", current=1, receiveDateEnd="$None$", useStatus="$None$", rightsType="$None$", mobile="$None$", rightsOrderId="$None$", size=10, _assert=True,  **kwargs):
        """
            url=/order/rightsOrder/page
                params: size :  :
                params: current :  :
                params: mobile :  : 手机号码
                params: rightsOrderId :  : 权益订单ID
                params: orderMainId :  : 主订单ID
                params: useStatus :  : 权益使用状态
                params: rightsType :  : 权益类型
                params: receiveDateBegin :  : 权益领取时间 开始
                params: receiveDateEnd :  : 权益领取时间-结束
                params: payDateBegin :  : 权益支付时间 - 开始
                params: payDateEnd :  : 权益支付时间 - 结束
                params: headers : 请求头
        """
        payDateBegin = self.get_list_choice(payDateBegin, list_or_dict=None, key="payDateBegin")
        userId = self.get_list_choice(userId, list_or_dict=None, key="userId")
        orderMainId = self.get_list_choice(orderMainId, list_or_dict=None, key="orderMainId")
        payDateEnd = self.get_list_choice(payDateEnd, list_or_dict=None, key="payDateEnd")
        receiveDateBegin = self.get_list_choice(receiveDateBegin, list_or_dict=None, key="receiveDateBegin")
        receiveDateEnd = self.get_list_choice(receiveDateEnd, list_or_dict=None, key="receiveDateEnd")
        useStatus = self.get_list_choice(useStatus, list_or_dict=None, key="useStatus")
        rightsType = self.get_list_choice(rightsType, list_or_dict=None, key="rightsType")
        mobile = self.get_list_choice(mobile, list_or_dict=None, key="mobile")
        rightsOrderId = self.get_list_choice(rightsOrderId, list_or_dict=None, key="rightsOrderId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_rightsorder.order_rightsorder_page(**_kwargs)

        self.assert_order_rightsorder_page(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="权益-领取权益-Y")
    def order_rightsorder_receive(self, orderId="$None$", rightsId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/order/rightsOrder/receive
                params: orderId : string : 子订单ID
                params: rightsId : number : 权益ID
                params: headers : 请求头
        """
        orderId = self.get_value_choice(orderId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        rightsId = self.get_value_choice(rightsId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_rightsorder.order_rightsorder_receive(**_kwargs)

        self.assert_order_rightsorder_receive(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="权益订单 - 查询-Y")
    def order_rightsorder_getorderlist(self, useStatusList="$None$", orderMainId="$None$", rightsType="$None$", rightsNameList="$None$", mobile="$None$", receiveDate="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/order/rightsOrder/getOrderList
                params: orderMainId : number : 主订单ID
                params: rightsType : integer : 权益类型
                params: rightsNameList : array : 权益名称
                type : string : None
                params: useStatusList : array : 权益使用状态
                type : integer : None
                params: mobile : string : 用户手机号
                params: receiveDate : string : 权益领取时间
                params: headers : 请求头
        """
        useStatusList = self.get_value_choice(useStatusList, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        orderMainId = self.get_value_choice(orderMainId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        rightsType = self.get_value_choice(rightsType, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        rightsNameList = self.get_value_choice(rightsNameList, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        mobile = self.get_value_choice(mobile, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        receiveDate = self.get_value_choice(receiveDate, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_rightsorder.order_rightsorder_getorderlist(**_kwargs)

        self.assert_order_rightsorder_getorderlist(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="更新充电桩订单状态-Y")
    def order_rightsorder_statusupdate(self, workStatus="$None$", soNo="$None$", _assert=True,  **kwargs):
        """
            url=/order/rightsOrder/statusUpdate
                params: soNo :  : 第三方订单
                params: workStatus :  : 权益使用状态
                params: headers : 请求头
        """
        workStatus = self.get_list_choice(workStatus, list_or_dict=None, key="workStatus")
        soNo = self.get_list_choice(soNo, list_or_dict=None, key="soNo")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_rightsorder.order_rightsorder_statusupdate(**_kwargs)

        self.assert_order_rightsorder_statusupdate(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


