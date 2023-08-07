import allure

from service.app_a.asserts.order.rightsorder.asserts_order_rightsorder_receive import AssertsOrderRightsorderReceive
from service.app_a.apis.order.rightsorder import apis_order_rightsorder_receive


class FunsOrderRightsorderReceive(AssertsOrderRightsorderReceive):
    @allure.step(title="权益-编辑权益订单-Y")
    def order_rightsorder_receive_update(self, orderMainId="$None$", userId="$None$", rightsId="$None$", createBy="$None$", payDate="$None$", createTime="$None$", refundDate="$None$", payBillNo="$None$", useStatus="$None$", rightsType="$None$", rightsName="$None$", payAmount="$None$", mobile="$None$", receiveDate="$None$", refundBillNo="$None$", updateId="$None$", updateTime="$None$", rightsOrderId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/order/rightsOrder/receive/update
                params: rightsOrderId : string :
                params: rightsId : string :
                params: rightsType : string :
                params: rightsName : string :
                params: orderMainId : string :
                params: mobile : string :
                params: payAmount : string :
                params: useStatus : string :
                params: receiveDate : string :
                params: payDate : string :
                params: refundDate : string :
                params: payBillNo : string :
                params: refundBillNo : string :
                params: createTime : string :
                params: createBy : string :
                params: updateTime : string :
                params: updateId : string :
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
        self.res = apis_order_rightsorder_receive.order_rightsorder_receive_update(**_kwargs)

        self.assert_order_rightsorder_receive_update(_assert, **_kwargs)
        self.set_value(_kwargs)


