import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/goods/configure/saveCarConfigure")
def goods_configure_savecarconfigure(salesVersionList=None, optionalList=None, appearanceColorList=None, interiorColorList=None, processColorList=None, headers=None, **kwargs):
    """
    保存车型配置信息-Y
    up_time=1675650535

    params: salesVersionList : array : 销售版本
              configureId : string : 配置ID
              modelId : string : 关联的车型基础信息ID
              configureCode : string : 配置编码
              configureName : string : 配置名称
              saleVersion : string : 销售-版本号
              abbreviationList : array : 缩略图
              gwAbbreviationList : array : 官网缩略图
              defaultCarModelList : array : 默认车型
              gwDefaultCarModelList : array : 官网默认车型
              price : number : 零售价|加价
              sort : number : 前台权重
              versionDesc : string : 版本描述
              partsDesc : string : 配件描述
              status : number : 状态 （1:启用，0：禁用） 默认启用
              type : number : 1:销售版本,2:动力系统,3:外观颜色,4:内饰颜色,5:选装配置
    params: processColorList : array : 套色
              configureId : string : 配置ID
              modelId : string : 车型ID
              configureCode : string : 配置编码
              configureName : string : 配置名称
              saleVersionRelation : string : 关联销售版本 ALL代表全部多个版本以英文逗号隔开
              appearanceColorRelation : string : 套色、内饰关联的外观颜色，ALL代表全部多个版本以英文逗号隔开
              saleVersionContain : string : 价格已包含的版本， ALL代表全部多个版本以英文逗号隔开
              modificationName : string : 外观颜色|套色|内饰颜色|选装名称 - 修饰名称
              abbreviationList : array : 缩略图
              gwAbbreviationList : array : 官网缩略图
              defaultCarModelList : array : 默认车型
              gwDefaultCarModelList : array : 官网默认车型
              price : number : 加价
              sort : number : 排序
              versionDesc : string : 
              partsDesc : string : 
              status : number : 状态
              type : number : 类型
    params: appearanceColorList : array : 外观颜色
              configureId : string : 配置Id
              modelId : string : 车型ID
              configureCode : string : 配置编码
              configureName : string : 配置名称
              saleVersionRelation : string : 关联销售版本 ALL代表全部多个版本以英文逗号隔开
              appearanceColorRelation : string : 套色、内饰关联的外观颜色，ALL代表全部多个版本以英文逗号隔开
              saleVersionContain : string : 价格已包含的版本， ALL代表全部多个版本以英文逗号隔开
              modificationName : string : 外观颜色|套色|内饰颜色|选装名称 - 修饰名称
              abbreviationList : array : 缩略图
              gwAbbreviationList : array : 官网缩略图
              defaultCarModelList : array : 默认车型
              gwDefaultCarModelList : array : 官网默认车型
              price : number : 加价
              sort : number : 排序
              versionDesc : string : 
              partsDesc : string : 
              status : number : 状态
              type : number : 类型
    params: interiorColorList : array : 内饰颜色
              configureId : string : 配置ID
              modelId : string : 车型Id
              configureCode : string : 配置编码
              configureName : string : 配置名称
              saleVersionRelation : string : 关联销售版本 ALL代表全部多个版本以英文逗号隔开
              appearanceColorRelation : string : 套色、内饰关联的外观颜色，ALL代表全部多个版本以英文逗号隔开
              saleVersionContain : string : 价格已包含的版本， ALL代表全部多个版本以英文逗号隔开
              modificationName : string : 外观颜色|套色|内饰颜色|选装名称 - 修饰名称
              abbreviationList : array : 缩略图
              gwAbbreviationList : array : 官网缩略图
              defaultCarModelList : array : 默认车型
              gwDefaultCarModelList : array : 官网默认车型
              price : number : 加价
              sort : number : 排序
              versionDesc : string : 
              partsDesc : string : 
              status : number : 状态
              type : number : 类型
    params: optionalList : array : 选装配件
              configureId : string : 配置ID
              modelId : string : 车型ID
              configureCode : string : 配置编码
              configureName : string : 配置名称
              saleVersionRelation : string : 关联销售版本 ALL代表全部多个版本以英文逗号隔开
              appearanceColorRelation : string : 套色、内饰关联的外观颜色，ALL代表全部多个版本以英文逗号隔开
              saleVersionContain : string : 价格已包含的版本， ALL代表全部多个版本以英文逗号隔开
              modificationName : string : 外观颜色|套色|内饰颜色|选装名称 - 修饰名称
              abbreviationList : array : 缩略图
              gwAbbreviationList : array : 官网缩略图
              defaultCarModelList : array : 默认车型
              gwDefaultCarModelList : array : 官网默认车型
              price : number : 加价
              sort : number : 排序
              versionDesc : string : 
              partsDesc : string : 配件描述
              status : number : 状态 默认启用 1
              type : number : 1:销售版本,2:外观颜色,3:套色,4:内饰颜色,5:选装配置
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/goods/configure/saveCarConfigure"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "salesVersionList": salesVersionList,  # 销售版本
        "processColorList": processColorList,  # 套色
        "appearanceColorList": appearanceColorList,  # 外观颜色
        "interiorColorList": interiorColorList,  # 内饰颜色
        "optionalList": optionalList,  # 选装配件
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/configure/getCarConfigureName")
def goods_configure_getcarconfigurename(modelId=None, headers=None, **kwargs):
    """
    查询配置名称-Y
    up_time=1675652068

    params: modelId :  : 车型Id
    params: headers : 请求头
    ====================返回======================
    params: code : number : 编码
    params: msg : string : 消息
    params: data : object : 数据
              salesVersion : array : 销售版本
              optional : array : 选装
              optionalPackage : array : 选装包
              appearanceColor : array : 外观颜色
    """
    _method = "GET"
    _url = "/goods/configure/getCarConfigureName"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "modelId": modelId,  # 车型Id
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/configure/removeCarConfigure")
def goods_configure_removecarconfigure(configureId=None, headers=None, **kwargs):
    """
    车型配置删除-D
    up_time=1675650781

    params: configureId :  : 主键Id
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : null : 
    """
    _method = "GET"
    _url = "/goods/configure/removeCarConfigure"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "configureId": configureId,  # 主键Id
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/configure/updateCarConfigureStatus")
def goods_configure_updatecarconfigurestatus(configureId=None, headers=None, **kwargs):
    """
    车型配置更改状态-D
    up_time=1675650743

    params: configureId :  : 车型配置Id
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "GET"
    _url = "/goods/configure/updateCarConfigureStatus"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "configureId": configureId,  # 车型配置Id
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/configure/info")
def goods_configure_info(modelId=None, headers=None, **kwargs):
    """
    车型配置查询（930）-?
    up_time=1675391059

    params: modelId :  : 车型基础ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 编码
    params: msg : string : 信息
    params: data : object : 数据
              interiorColor : array : 内饰颜色
              processColor : array : 套色
              appearanceColor : array : 外观颜色
              salesVersion : array : 销售版本
              optional : array : 选配
    """
    _method = "GET"
    _url = "/goods/configure/info"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "modelId": modelId,  # 车型基础ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


