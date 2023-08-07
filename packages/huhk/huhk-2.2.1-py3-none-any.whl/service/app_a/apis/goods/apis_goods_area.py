import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/goods/area/getParentArea")
def goods_area_getparentarea(parentId=None, country=None, headers=None, **kwargs):
    """
    订单管理-地区下拉（930版本）-Y
    up_time=1675385800

    params: parentId :  : 父地区id（null 则省，下一级递增）
    params: country :  : all会加上全国信息
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : array : 
              areaId : number : 地区id
              areaName : string : 区域名称
              areaLevel : number : 区域级别： 1  省份， 2  市， 3  区县
              parentId : integer : 父级id
              areaType : number : 0:全面解禁，1:部分解禁，2:禁行
              areaPyName : string : 中文拼音
              dealerCodeList : array : 经销商ID
              dealerCodes : ['string', 'null'] : 经销商ID
    """
    _method = "GET"
    _url = "/goods/area/getParentArea"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "parentId": parentId,  # 父地区id（null 则省，下一级递增）
        "country": country,  # all会加上全国信息
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/area/getDefaultDealer")
def goods_area_getdefaultdealer(cityCode=None, headers=None, **kwargs):
    """
    pc端查询城市默认经销商-Y
    up_time=1675389643

    params: cityCode :  : 城市编码
    params: headers : 请求头
    ====================返回======================
    params: code : number : 编码
    params: msg : string : 消息
    params: data : object : 数据
              areaIds : array : 
              dealerCode : string : 经销商编码
              dealerName : string : 经销商名称
              companyName : string : 
              companyCode : string : 
    """
    _method = "GET"
    _url = "/goods/area/getDefaultDealer"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "cityCode": cityCode,  # 城市编码
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/area/insertRelation")
def goods_area_insertrelation(areaIds=None, dealerCode=None, headers=None, **kwargs):
    """
    后台管理-设置默认经销商-Y
    up_time=1675389550

    params: areaIds : array : 地区集合
              type : integer : None
              description : 地区Id : None
    params: dealerCode : string : 进销商编码
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : true
    """
    _method = "POST"
    _url = "/goods/area/insertRelation"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "areaIds": areaIds,  # 地区集合
        "dealerCode": dealerCode,  # 进销商编码
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/area/getCityList")
def goods_area_getcitylist(cName=None, current=None, pName=None, cType=None, size=None, headers=None, **kwargs):
    """
    城市禁行列表查询-Y
    up_time=1675388494

    params: size :  : 当前页数量
    params: current :  : 当前页号
    params: pName :  : 省份名称
    params: cName :  : 城市名称
    params: cType :  : 城市禁行类型 0:全面解禁，1:部分解禁，2:禁行  
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
    _url = "/goods/area/getCityList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "size": size,  # 当前页数量
        "current": current,  # 当前页号
        "pName": pName,  # 省份名称
        "cName": cName,  # 城市名称
        "cType": cType,  # 城市禁行类型 0:全面解禁，1:部分解禁，2:禁行  
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/area/getCityById")
def goods_area_getcitybyid(cityId=None, headers=None, **kwargs):
    """
    查询禁行城市信息-Y
    up_time=1675388979

    params: cityId :  : 城市编码
    params: headers : 请求头
    ====================返回======================
    params: code : number : 编码
    params: msg : string : 消息
    params: data : object : 数据
              areaId : number : 编码
              areaName : string : 名称
              areaLevel : number : 级别
              parentId : number : 父类编码
              areaType : number : 城市禁行类型      0:全面解禁，1:部分解禁，2:禁行
              areaPyName : string : 中文拼音
    """
    _method = "GET"
    _url = "/goods/area/getCityById"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "cityId": cityId,  # 城市编码
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/area/getMapArea")
def goods_area_getmaparea(parentId=None, headers=None, **kwargs):
    """
    地区下拉待字母（930）-?
    up_time=1675387893

    params: parentId :  : 地区Id（省传null ，其余传areaId的值）
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              A : array : 字母
              B : array : 
              C : array : 
              F : array : 
              G : array : 
              H : array : 
              J : array : 
              L : array : 
              N : array : 
              Q : array : 
              S : array : 
              T : array : 
              X : array : 
              Y : array : 
              Z : array : 
    """
    _method = "GET"
    _url = "/goods/area/getMapArea"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "parentId": parentId,  # 地区Id（省传null ，其余传areaId的值）
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/area/getCity")
def goods_area_getcity(parentId=None, headers=None, **kwargs):
    """
    城市下拉带字母（930）-？
    up_time=1675388144

    params: parentId :  : 父级ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              A : array : 字母
              B : array : 字母
              C : array : 字母
              D : array : 字母
              E : array : 字母
              F : array : 字母
              G : array : 字母
              H : array : 字母
              J : array : 字母
              K : array : 字母
              L : array : 字母
              M : array : 字母
              N : array : 字母
              P : array : 字母
              Q : array : 字母
              R : array : 字母
              S : array : 字母
              T : array : 字母
              W : array : 字母
              X : array : 字母
              Y : array : 字母
              Z : array : 字母
    """
    _method = "GET"
    _url = "/goods/area/getCity"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "parentId": parentId,  # 父级ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/area/updateCityType")
def goods_area_updatecitytype(cType=None, cId=None, headers=None, **kwargs):
    """
    城市禁行状态变更-？
    up_time=1675388620

    params: cType : integer : 禁用类型
    params: cId : integer : 城市编码
    params: headers : 请求头
    ====================返回======================
    params: code : number : 编码
    params: msg : string : 消息
    params: data : boolean : true|false
    """
    _method = "POST"
    _url = "/goods/area/updateCityType"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "cType": cType,  # 禁用类型
        "cId": cId,  # 城市编码
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


