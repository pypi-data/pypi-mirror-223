import allure

from service.app_a.funs.funs_app_a import FunsAppA


@allure.epic("接口测试")
@allure.feature("场景：接口（/page）")
class TestPage:
    def setup(self):
        self.f = FunsAppA()

    # @pytest.mark.skip("不执行")
    @allure.step(title="网点列表-获取经销商")
    def test_page_001(self):
        self.f.page()

    # @pytest.mark.skip("不执行")
    @allure.step(title="网点列表-获取经销商__翻页")
    def test_page__current_002(self):
        self.f.page(current=2)

    # @pytest.mark.skip("不执行")
    @allure.step(title="网点列表-获取经销商__每页条数")
    def test_page__size_003(self):
        self.f.page(size=20)

    # @pytest.mark.skip("不执行")
    @allure.step(title="网点列表-获取经销商__单参数有值： districtNameSort")
    def test_page__districtNameSort_004(self):
        self.f.page(districtNameSort=True)

    # @pytest.mark.skip("不执行")
    @allure.step(title="网点列表-获取经销商__单参数有值： dealerName")
    def test_page__dealerName_005(self):
        self.f.page(dealerName=True)

    # @pytest.mark.skip("不执行")
    @allure.step(title="网点列表-获取经销商__单参数有值： shopBusinessType")
    def test_page__shopBusinessType_006(self):
        self.f.page(shopBusinessType=True)

    # @pytest.mark.skip("不执行")
    @allure.step(title="网点列表-获取经销商__单参数有值： provinceNameSort")
    def test_page__provinceNameSort_007(self):
        self.f.page(provinceNameSort=True)

    # @pytest.mark.skip("不执行")
    @allure.step(title="网点列表-获取经销商__单参数有值： dealerCode")
    def test_page__dealerCode_008(self):
        self.f.page(dealerCode=True)

    # @pytest.mark.skip("不执行")
    @allure.step(title="网点列表-获取经销商__单参数有值： province")
    def test_page__province_009(self):
        self.f.page(province=True)

    # @pytest.mark.skip("不执行")
    @allure.step(title="网点列表-获取经销商__单参数有值： city")
    def test_page__city_010(self):
        self.f.page(city=True)

    # @pytest.mark.skip("不执行")
    @allure.step(title="网点列表-获取经销商__单参数有值： district")
    def test_page__district_011(self):
        self.f.page(district=True)

    # @pytest.mark.skip("不执行")
    @allure.step(title="网点列表-获取经销商__单参数有值： cityNameSort")
    def test_page__cityNameSort_012(self):
        self.f.page(cityNameSort=True)

    # @pytest.mark.skip("不执行")
    @allure.step(title="网点列表-获取经销商__单参数有值： dealerAddress")
    def test_page__dealerAddress_013(self):
        self.f.page(dealerAddress=True)

    # @pytest.mark.skip("不执行")
    @allure.step(title="网点列表-获取经销商__所有参数有值")
    def test_page__all_014(self):
        self.f.page(districtNameSort=True, dealerName=True, shopBusinessType=True, provinceNameSort=True, dealerCode=True, province=True, city=True, district=True, cityNameSort=True, dealerAddress=True)

