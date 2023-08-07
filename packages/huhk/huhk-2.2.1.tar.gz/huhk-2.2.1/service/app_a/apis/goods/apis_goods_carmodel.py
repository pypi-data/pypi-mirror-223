import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/goods/carmodel/saveManageCarModel")
def goods_carmodel_savemanagecarmodel(prePricePosters=None, modelCode=None, price=None, status=None, posters=None, preEndTime=None, modelName=None, promptDesc=None, prePrice=None, carDetailPics=None, preToDepositEndTime=None, depositStartTime=None, carSimpleName=None, depositPrice=None, sharePosters=None, brandName=None, preStartTime=None, depositPriceContent=None, version=None, carName=None, configCode=None, depositEndTime=None, prePriceContent=None, preToDepositStartTime=None, modelId=None, carCode=None, carDetailType=None, carDetailUrl=None, sort=None, headers=None, **kwargs):
    """
    保存车型详细信息 - Y
    up_time=1675664128

    params: carName : string : 车系名称
    params: brandName : string : 品牌名称
    params: version : string : 品牌代码
    params: carCode : string : 车系代码
    params: modelName : string : 车型名称
    params: modelCode : string : 车型代号
    params: carSimpleName : string : 车型销售名称
    params: configCode : string : 配置编码
    params: sort : number : 车型权重
    params: price : number : 基础零售价
    params: carDetailType : number : 车型详情类型 - 1:图片，2:H5连接
    params: carDetailUrl : string : 车型详情类型为2 h5跳转地址
    params: preStartTime : string : 预订开始时间
    params: preEndTime : string : 预订结束时间
    params: preToDepositStartTime : string : 预订转大定开始时间
    params: preToDepositEndTime : string : 预订转大定结束时间
    params: prePrice : number : 预订金价格
    params: prePriceContent : string : 预订权益内容
    params: depositStartTime : string : 大定开始时间
    params: depositEndTime : string : 大定结束时间
    params: depositPrice : number : 定金价格
    params: depositPriceContent : string : 定金权益内容
    params: posters : array : 爱车海报
              imageUrl : string : 图片地址
              modelId : string : 车型ID
    params: sharePosters : array : 分享海报
              imageUrl : string : 
              modelId : string : 
    params: carDetailPics : array : 车详情图片
              imageUrl : string : 
              modelId : string : 
    params: prePricePosters : array : 预订金海报
              imageUrl : string : 
              modelId : string : 
    params: promptDesc : string : 提示文案
    params: modelId : string : 车型ID
    params: status : number : 状态(0禁用1启用)
    params: headers : 请求头
    ====================返回======================
    params: code : string : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/goods/carmodel/saveManageCarModel"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "carName": carName,  # 车系名称
        "brandName": brandName,  # 品牌名称
        "version": version,  # 品牌代码
        "carCode": carCode,  # 车系代码
        "modelName": modelName,  # 车型名称
        "modelCode": modelCode,  # 车型代号
        "carSimpleName": carSimpleName,  # 车型销售名称
        "configCode": configCode,  # 配置编码
        "sort": sort,  # 车型权重
        "price": price,  # 基础零售价
        "carDetailType": carDetailType,  # 车型详情类型 - 1:图片，2:H5连接
        "carDetailUrl": carDetailUrl,  # 车型详情类型为2 h5跳转地址
        "preStartTime": preStartTime,  # 预订开始时间
        "preEndTime": preEndTime,  # 预订结束时间
        "preToDepositStartTime": preToDepositStartTime,  # 预订转大定开始时间
        "preToDepositEndTime": preToDepositEndTime,  # 预订转大定结束时间
        "prePrice": prePrice,  # 预订金价格
        "prePriceContent": prePriceContent,  # 预订权益内容
        "depositStartTime": depositStartTime,  # 大定开始时间
        "depositEndTime": depositEndTime,  # 大定结束时间
        "depositPrice": depositPrice,  # 定金价格
        "depositPriceContent": depositPriceContent,  # 定金权益内容
        "posters": posters,  # 爱车海报
        "sharePosters": sharePosters,  # 分享海报
        "carDetailPics": carDetailPics,  # 车详情图片
        "prePricePosters": prePricePosters,  # 预订金海报
        "promptDesc": promptDesc,  # 提示文案
        "modelId": modelId,  # 车型ID
        "status": status,  # 状态(0禁用1启用)
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/carmodel/removeById")
def goods_carmodel_removebyid(modelId=None, headers=None, **kwargs):
    """
    删除车型-Y
    up_time=1675660050

    params: modelId :  : 车型id
    params: headers : 请求头
    ====================返回======================
    params: code : string : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "GET"
    _url = "/goods/carmodel/removeById"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "modelId": modelId,  # 车型id
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/carmodel/getCarModelManageById")
def goods_carmodel_getcarmodelmanagebyid(modelId=None, headers=None, **kwargs):
    """
    查询车型详细信息-Y
    up_time=1675663920

    params: modelId :  : 车型编码
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              statusName : string : 状态(0.禁用 1.启用 2.删除)
              commodityWebUrl : string : 商品地址
              optional : string : 配置与选装
              appearances : array : 外观
              trims : array : 
              posters : array : 爱车海报
              sharePosters : array : 分享海报
              carDetailPics : array : 车型详情类型 - 1：车详情图片
              prePricePosters : array : 预订金海报
              carModelBatteries : array : 
              carModelItems : array : 
              dType : integer : 前端展示哪个订（定）  处于小订 为 0 处于大定 1 非此两个阶段是 2
    """
    _method = "GET"
    _url = "/goods/carmodel/getCarModelManageById"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "modelId": modelId,  # 车型编码
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/carmodel/getManageCarModel")
def goods_carmodel_getmanagecarmodel(carName=None, modelCode=None, brandName=None, current=None, status=None, carCode=None, version=None, operator=None, modelName=None, size=None, headers=None, **kwargs):
    """
    车型列表-Y
    up_time=1675661996

    params: current :  : 分页
    params: size :  : 分页
    params: modelName :  : 车型名称
    params: modelCode :  : 车型代号
    params: status :  : 0:待启用，1:启用，2:禁用 车型新增默认状态待启用，全部则不传值
    params: operator :  : 操作人
    params: brandName :  : 品牌名称
    params: version :  : 品牌编码
    params: carName :  : 车系名称
    params: carCode :  : 车型编码
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
              countId : number : 
              maxLimit : number : 
              pages : number : 
    """
    _method = "GET"
    _url = "/goods/carmodel/getManageCarModel"

    _headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,  # 分页
        "size": size,  # 分页
        "modelName": modelName,  # 车型名称
        "modelCode": modelCode,  # 车型代号
        "status": status,  # 0:待启用，1:启用，2:禁用 车型新增默认状态待启用，全部则不传值
        "operator": operator,  # 操作人
        "brandName": brandName,  # 品牌名称
        "version": version,  # 品牌编码
        "carName": carName,  # 车系名称
        "carCode": carCode,  # 车型编码
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/carmodel/getModelNameList")
def goods_carmodel_getmodelnamelist( headers=None, **kwargs):
    """
    订单管理-查询可试驾车型-Y
    up_time=1675234063

    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : array : 
              modelId : string : 
              brandName : string : 
              version : string : 
              carName : string : 
              carCode : string : 
              modelName : string : 
              modelCode : string : 
              carSimpleName : string : 
              configCode : string : 
              sort : number : 
              price : number : 
              carDetailType : number : 
              carDetailUrl : string : 
              preStartTime : string : 
              preEndTime : string : 
              preToDepositStartTime : string : 
              preToDepositEndTime : string : 
              prePrice : number : 
              prePriceContent : string : 
              depositStartTime : string : 
              depositEndTime : string : 
              depositPrice : number : 
              depositPriceContent : string : 
              status : number : 
              createBy : string : 
              createTime : string : 
              updateBy : string : 
              updateTime : string : 
              financeDesc : null : 
              modelDesc : null : 
              announcementCode : null : 
              listingTime : null : 
              setOfCars : null : 
              modelImageUrl : null : 
              operator : null : 
              createByName : null : 
              updateByName : null : 
    """
    _method = "GET"
    _url = "/goods/carmodel/getModelNameList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/carmodel/getCarNameList")
def goods_carmodel_getcarnamelist( headers=None, **kwargs):
    """
    车型下拉列表-Y
    up_time=1675659976

    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : array : 车型名称集合
              type : string : None
              description : 车型名称 : None
    """
    _method = "GET"
    _url = "/goods/carmodel/getCarNameList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


