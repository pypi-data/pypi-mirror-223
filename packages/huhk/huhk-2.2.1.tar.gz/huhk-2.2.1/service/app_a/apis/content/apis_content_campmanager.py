import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/campManager/page")
def content_campmanager_page(createBy=None, id=None, status=None, sortBody=None, sortord=None, name=None, headers=None, **kwargs):
    """
    营地服务列表 - 分页查询
    up_time=1681969132

    params: id :  : 
    params: name :  : 
    params: status :  : 
    params: createBy :  : 
    params: sortBody :  : 
    params: sortord :  : ASC/DESC/asc/desc
    params: headers : 请求头
    ====================返回======================
    params: code : number : 接口状态
    params: msg : string : 提示信息
    params: data : object : 
              id : string : 营地服务id
              name : string : 营地名称
              content : string : 营地简介
              campDetail : string : 营地详情
              url : string : 营地图片
              status : number : 1已上架 0已下架
              commentCnt : number : 评论量
              thumbsCnt : number : 点赞量
              createBy : string : 创建人
              updateTime : string : 上架时间
    """
    _method = "GET"
    _url = "/content/campManager/page"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "id": id,
        "name": name,
        "status": status,
        "createBy": createBy,
        "sortBody": sortBody,
        "sortord": sortord,  # ASC/DESC/asc/desc
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/campManager/soldOut")
def content_campmanager_soldout(campId=None, id=None, headers=None, **kwargs):
    """
    营地列表 - 下架/批量下架
    up_time=1681959868

    params: id :  : 
    params: campId : array : 营地服务ID
              type : string : None
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : string : 操作成功
    """
    _method = "PUT"
    _url = "/content/campManager/soldOut"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "id": id,
        "campId": campId,  # 营地服务ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/campManager/insertCampID")
def content_campmanager_insertcampid( headers=None, **kwargs):
    """
    新增营地 - 新增营地ID带出
    up_time=1681960296

    params: headers : 请求头
    ====================返回======================
    params: code : string : 
    params: msg : string : 
    params: data : string : 营地服务ID
    """
    _method = "GET"
    _url = "/content/campManager/insertCampID"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/campManager/insert")
def content_campmanager_insert(content=None, id=None, county=None, url=None, province=None, city=None, campTradeTime=None, campDetail=None, address=None, ownerDiscount=None, discountExpEndTime=None, discountExpBeginTime=None, name=None, headers=None, **kwargs):
    """
    新增营地
    up_time=1681967827

    params: id : text : 营地服务ID
    params: name : text : 营地名称
    params: content : text : 营地简介
    params: url : text : 营地图片
    params: campDetail : text : 营地详情
    params: ownerDiscount : text : 车主优惠
    params: campTradeTime : text : 营地营业时间
    params: discountExpBeginTime : text : 车主优惠有效期 - 开始时间
    params: discountExpEndTime : text : 车主优惠有效期 - 结束时间
    params: province : text : 省
    params: city : text : 市
    params: county : text : 区/县
    params: address : text : 详细地址
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : string : 新增成功
    """
    _method = "POST"
    _url = "/content/campManager/insert"

    _headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    _headers.update({"headers": headers})

    _data = {
        "id": id,  # 营地服务ID
        "name": name,  # 营地名称
        "content": content,  # 营地简介
        "url": url,  # 营地图片
        "campDetail": campDetail,  # 营地详情
        "ownerDiscount": ownerDiscount,  # 车主优惠
        "campTradeTime": campTradeTime,  # 营地营业时间
        "discountExpBeginTime": discountExpBeginTime,  # 车主优惠有效期 - 开始时间
        "discountExpEndTime": discountExpEndTime,  # 车主优惠有效期 - 结束时间
        "province": province,  # 省
        "city": city,  # 市
        "county": county,  # 区/县
        "address": address,  # 详细地址
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/campManager/detail/")
def content_campmanager_detail_(id=None, headers=None, **kwargs):
    """
    营地列表 - 营地详情
    up_time=1681969814

    params: id :  : 营地服务ID
    params: headers : 请求头
    ====================返回======================
    params: code : string : 
    params: msg : string : 
    params: data : object : 
              id : string : 营地服务id
              name : string : 营地名称
              content : string : 营地简介
              campDetail : string : 营地详情
              url : string : 营地图片
              ownerDiscount : string : 车主优惠
              campTradeTime : string : 营地营业时间
              discountExpBeginTime : string : 车主优惠有效期 - 开始时间
              discountExpEndTime : string : 车主优惠有效期 - 结束时间
              province : string : 省
              city : string : 市
              county : string : 区/县
              address : string : 详细地址
    """
    _method = "GET"
    _url = "/content/campManager/detail/{id}"
    _url = get_url(_url, locals())

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
        "id": id,  # 营地服务ID
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/campManager/update")
def content_campmanager_update(phone=None, areaCode=None, ownerDiscount=None, discountExpEndTime=None, discountExpBeginTime=None, headers=None, **kwargs):
    """
    编辑营地
    up_time=1681969876

    params: ownerDiscount : text : 车主优惠
    params: discountExpBeginTime : text : 车主优惠有效期 - 开始时间
    params: discountExpEndTime : text : 车主优惠有效期 - 结束时间
    params: areaCode : text : 区号
    params: phone : text : 手机号
    params: headers : 请求头
    ====================返回======================
    params: code : string : 
    params: msg : string : 
    params: data : string : 编辑成功
    """
    _method = "POST"
    _url = "/content/campManager/update"

    _headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    _headers.update({"headers": headers})

    _data = {
        "ownerDiscount": ownerDiscount,  # 车主优惠
        "discountExpBeginTime": discountExpBeginTime,  # 车主优惠有效期 - 开始时间
        "discountExpEndTime": discountExpEndTime,  # 车主优惠有效期 - 结束时间
        "areaCode": areaCode,  # 区号
        "phone": phone,  # 手机号
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


