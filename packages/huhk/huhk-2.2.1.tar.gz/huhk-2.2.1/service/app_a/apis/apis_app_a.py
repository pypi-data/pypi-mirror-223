import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/page")
def page(districtNameSort=None, dealerName=None, shopBusinessType=None, provinceNameSort=None, current=None, dealerCode=None, province=None, city=None, district=None, cityNameSort=None, dealerAddress=None, size=None, headers=None, **kwargs):
    """
    网点列表-获取经销商
    up_time=1675233719

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
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              records : array : 
              total : number : 
              size : number : 
              current : number : 
              orders : array : 
              optimizeCountSql : boolean : 
              searchCount : boolean : 
              countId : null : 
              maxLimit : null : 
              pages : number : 
    """
    _method = "GET"
    _url = "/page"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,
        "size": size,
        "province": province,
        "city": city,
        "district": district,
        "dealerCode": dealerCode,
        "dealerName": dealerName,
        "dealerAddress": dealerAddress,
        "shopBusinessType": shopBusinessType,
        "cityNameSort": cityNameSort,
        "districtNameSort": districtNameSort,
        "provinceNameSort": provinceNameSort,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


