from service.app_a.apis import apis_app_a
from service.app_a.asserts.asserts_app_a import AssertsAppA
import allure
from service.app_a.funs.funs_order import FunsOrder
from service.app_a.funs.funs_open import FunsOpen
from service.app_a.funs.funs_content import FunsContent
from service.app_a.funs.funs_admin import FunsAdmin
from service.app_a.funs.funs_common import FunsCommon
from service.app_a.funs.funs_goods import FunsGoods
from service.app_a.funs.funs_activitymanager import FunsActivitymanager
from service.app_a.funs.funs_radarpoints import FunsRadarpoints
from service.app_a.funs.funs_pay import FunsPay
from service.app_a.funs.funs_testdrive import FunsTestdrive
from service.app_a.funs.funs_manageapi import FunsManageapi
from service.app_a.funs.funs_essay import FunsEssay
from service.app_a.funs.funs_area import FunsArea


class FunsAppA(FunsOrder, FunsOpen, FunsContent, FunsAdmin, FunsCommon, FunsGoods, FunsActivitymanager, FunsRadarpoints, FunsPay, FunsTestdrive, FunsManageapi, FunsEssay, AssertsAppA, FunsArea):
    @allure.step(title="网点列表-获取经销商")
    def page(self, districtNameSort="$None$", dealerName="$None$", shopBusinessType="$None$", provinceNameSort="$None$", current=1, dealerCode="$None$", province="$None$", city="$None$", district="$None$", cityNameSort="$None$", dealerAddress="$None$", size=10, _assert=True,  **kwargs):
        """
            url=/page
                params: current :  :
                params: size :  :
                params: province :  :
                params: city :  :
                params: district :  :
                params: dealerCode :  :
                params: dealerName :  :
                params: dealerAddress :  :
                params: shopBusinessType :  :
                params: cityNameSort :  :
                params: districtNameSort :  :
                params: provinceNameSort :  :
                params: headers : 请求头
        """
        districtNameSort = self.get_list_choice(districtNameSort, list_or_dict=None, key="districtNameSort")
        dealerName = self.get_list_choice(dealerName, list_or_dict=None, key="dealerName")
        shopBusinessType = self.get_list_choice(shopBusinessType, list_or_dict=None, key="shopBusinessType")
        provinceNameSort = self.get_list_choice(provinceNameSort, list_or_dict=None, key="provinceNameSort")
        dealerCode = self.get_list_choice(dealerCode, list_or_dict=None, key="dealerCode")
        province = self.get_list_choice(province, list_or_dict=None, key="province")
        city = self.get_list_choice(city, list_or_dict=None, key="city")
        district = self.get_list_choice(district, list_or_dict=None, key="district")
        cityNameSort = self.get_list_choice(cityNameSort, list_or_dict=None, key="cityNameSort")
        dealerAddress = self.get_list_choice(dealerAddress, list_or_dict=None, key="dealerAddress")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_app_a.page(**_kwargs)

        self.assert_page(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


