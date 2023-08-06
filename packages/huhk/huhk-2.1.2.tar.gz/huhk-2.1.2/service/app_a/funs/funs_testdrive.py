import allure

from service.app_a.asserts.asserts_testdrive import AssertsTestdrive
from service.app_a.apis import apis_testdrive


class FunsTestdrive(AssertsTestdrive):
    @allure.step(title="预约试驾")
    def testdrive_subscribe(self, appointmentTime="$None$", customerName="$None$", modelId="$None$", shopId="$None$", channel="$None$", leadSanSourceCode="$None$", leadSourceCode="$None$", shopName="$None$", model="$None$", activityCode="$None$", phoneNumber="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/testDrive/subscribe
                params: model : text : 试驾车型名称
                params: shopName : text : 门店名称
                params: customerName : text : 客户姓名、昵称
                params: phoneNumber : text : 预留手机号
                params: channel : text : 1:移动应用 2:小程序 3:官方网站
                params: modelId : text : 预约车型id
                params: shopId : text : 预约门店id
                params: appointmentTime : text : 预约时间
                params: activityCode : string : 活动代码
                params: leadSourceCode : string : 线索来源小类
                params: leadSanSourceCode : string : 线索来源三级小类
                params: headers : 请求头
        """
        appointmentTime = self.get_value_choice(appointmentTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        customerName = self.get_value_choice(customerName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        modelId = self.get_value_choice(modelId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        shopId = self.get_value_choice(shopId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        channel = self.get_value_choice(channel, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        leadSanSourceCode = self.get_value_choice(leadSanSourceCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        leadSourceCode = self.get_value_choice(leadSourceCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        shopName = self.get_value_choice(shopName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        model = self.get_value_choice(model, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        activityCode = self.get_value_choice(activityCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        phoneNumber = self.get_value_choice(phoneNumber, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_testdrive.testdrive_subscribe(**_kwargs)

        self.assert_testdrive_subscribe(_assert, **_kwargs)
        self.set_value(_kwargs)


