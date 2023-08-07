import allure

from service.app_a.asserts.order.asserts_order_freeorder import AssertsOrderFreeorder
from service.app_a.apis.order import apis_order_freeorder


class FunsOrderFreeorder(AssertsOrderFreeorder):
    @allure.step(title="导出0元订购预定信息表-Y")
    def order_freeorder_download(self, provinceName="$None$", freeOrderId="$None$", provinceId="$None$", regisTimeBegin="$None$", avatarUrl="$None$", createTime="$None$", nickName="$None$", modelId="$None$", userPolicyCode="$None$", channel="$None$", privacyPolicyCode="$None$", mobile="$None$", cityName="$None$", channelName="$None$", regisTimeEnd="$None$", cityId="$None$", userName="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/order/freeOrder/downLoad
                params: freeOrderId : integer : 订单号
                params: modelId : string : 车型编码
                params: userName : string : 用户姓名
                params: mobile : string : 用户号码
                params: provinceId : string : 省编码
                params: provinceName : string : 省
                params: cityId : string : 市编码
                params: cityName : string : 市
                params: channel : string : 渠道 0 官网 1 app
                params: channelName : string :
                params: createTime : string : 订单创建时间
                params: regisTimeBegin : string : 开始时间
                params: regisTimeEnd : string : 结束时间
                params: nickName : string : 昵称
                params: avatarUrl : string : 头像
                params: userPolicyCode : string : 用户协议版本号
                params: privacyPolicyCode : string : 隐私协议版本号
                params: headers : 请求头
        """
        provinceName = self.get_value_choice(provinceName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        freeOrderId = self.get_value_choice(freeOrderId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        provinceId = self.get_value_choice(provinceId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        regisTimeBegin = self.get_value_choice(regisTimeBegin, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        avatarUrl = self.get_value_choice(avatarUrl, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        createTime = self.get_value_choice(createTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        nickName = self.get_value_choice(nickName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        modelId = self.get_value_choice(modelId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        userPolicyCode = self.get_value_choice(userPolicyCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        channel = self.get_value_choice(channel, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        privacyPolicyCode = self.get_value_choice(privacyPolicyCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        mobile = self.get_value_choice(mobile, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        cityName = self.get_value_choice(cityName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        channelName = self.get_value_choice(channelName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        regisTimeEnd = self.get_value_choice(regisTimeEnd, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        cityId = self.get_value_choice(cityId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        userName = self.get_value_choice(userName, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_freeorder.order_freeorder_download(**_kwargs)

        self.assert_order_freeorder_download(_assert, **_kwargs)
        self.set_value(_kwargs)


