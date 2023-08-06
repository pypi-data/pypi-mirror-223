import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/adv/save")
def content_adv_save(advId=None, advText=None, jumpContent=None, advLinkUrl=None, bindingFlag=None, jumpType=None, version=None, advSerial=None, advPlaceId=None, advPicUrl=None, pictureList=None, headers=None, **kwargs):
    """
    点位内容-保存运营端配置(更新、新增)（930）-Y
    up_time=1675674291

    params: advPlaceId : number : 左侧列表选中ID
    params: advPicUrl : string : 图片地址
    params: advText : string : 文字描述
    params: advSerial : string : 排序
    params: jumpType : number : 跳转类型
    params: jumpContent : string : 跳转内容
    params: advId : number : 点位ID（更新时必传）
    params: version : string : 绑定的车系（60s,80v）
    params: advLinkUrl : string : 爱车海报填写地址/url跳转地址
    params: bindingFlag : number : 车辆绑定标识 1绑定 0未绑定
    params: pictureList : array : 当跳转类型为16：图片新增字段
              type : string : None
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功
    params: msg : string : 
    params: data : boolean : true成功
    """
    _method = "POST"
    _url = "/content/adv/save"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "advPlaceId": advPlaceId,  # 左侧列表选中ID
        "advPicUrl": advPicUrl,  # 图片地址
        "advText": advText,  # 文字描述
        "advSerial": advSerial,  # 排序
        "jumpType": jumpType,  # 跳转类型
        "jumpContent": jumpContent,  # 跳转内容
        "advId": advId,  # 点位ID（更新时必传）
        "version": version,  # 绑定的车系（60s,80v）
        "advLinkUrl": advLinkUrl,  # 爱车海报填写地址/url跳转地址
        "bindingFlag": bindingFlag,  # 车辆绑定标识 1绑定 0未绑定
        "pictureList": pictureList,  # 当跳转类型为16：图片新增字段
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/adv/updateEssayAdvList")
def content_adv_updateessayadvlist(essayId=None, headers=None, **kwargs):
    """
    点位内容-修改点位信息-Y
    up_time=1675674872

    params: essayId : string : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : string : 
    """
    _method = "POST"
    _url = "/content/adv/updateEssayAdvList"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "essayId": essayId,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/adv/setTopFlag")
def content_adv_settopflag(essayId=None, headers=None, **kwargs):
    """
    点位内容-文章置顶-Y
    up_time=1675673726

    params: essayId : text : 文章主键Id
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : string : 
    """
    _method = "POST"
    _url = "/content/adv/setTopFlag"

    _headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    _headers.update({"headers": headers})

    _data = {
        "essayId": essayId,  # 文章主键Id
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/adv/advPlaceList")
def content_adv_advplacelist(advPlaceId=None, headers=None, **kwargs):
    """
    点位内容-点位查询接口-Y
    up_time=1677046697

    params: advPlaceId :  : 广告点位主键：
【发现-推荐】轮播图
【发现-推荐】快捷入口
【发现-资讯】金刚区
【爱车】试驾页轮播
【发现-推荐】精选内容
【爱车-智能车控】
【爱车-购车帮助】
【我的-邀请好友】海报图
【我的-积分】积分规则说明
【爱车-购车帮助（新）】

    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : object : 
              records : array : 
              total : number : 
              size : number : 
              pages : number : 
    """
    _method = "GET"
    _url = "/content/adv/advPlaceList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "advPlaceId": advPlaceId,  # 广告点位主键： 【发现-推荐】轮播图 【发现-推荐】快捷入口 【发现-资讯】金刚区 【爱车】试驾页轮播 【发现-推荐】精选内容 【爱车-智能车控】 【爱车-购车帮助】 【我的-邀请好友】海报图 【我的-积分】积分规则说明 【爱车-购车帮助（新）】 
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/adv/delete")
def content_adv_delete(advId=None, headers=None, **kwargs):
    """
    点位内容-删除-Y
    up_time=1675674198

    params: advId : string : 点位ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功
    params: msg : string : 描述
    params: data : boolean : true成功
    """
    _method = "POST"
    _url = "/content/adv/delete"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "advId": advId,  # 点位ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/adv/detailAdmin")
def content_adv_detailadmin(advPlaceId=None, headers=None, **kwargs):
    """
    点位查询(930版本)-Y
    up_time=1675672243

    params: advPlaceId :  : 广告位id
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 数据
              advPlaceId : string : 点位D
              advPlaceName : string : 点位名称
              advPlaceType : number : 广告位类型 1：焦点图类型点位 2、导航类型点位 
              createTime : string : 
              createBy : string : 
              updateTime : string : 
              updateBy : string : 
              obj : null : 
              adv : null : 
              advList : array : 点位内容
    """
    _method = "GET"
    _url = "/content/adv/detailAdmin"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "advPlaceId": advPlaceId,  # 广告位id
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/adv/saveAll")
def content_adv_saveall(advPlaceId=None, jumpType=None, headers=None, **kwargs):
    """
    点位内容-新增广告位（点位）-Y
    up_time=1675674158

    params: advPlaceId : number : 广告位ID
    params: jumpType : integer : 备注中查看状态信息
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/adv/saveAll"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "advPlaceId": advPlaceId,  # 广告位ID
        "jumpType": jumpType,  # 备注中查看状态信息
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/adv/jumpContent")
def content_adv_jumpcontent(typeCode=None, keyWord=None, headers=None, **kwargs):
    """
    点位内容-根据跳转类型选择跳转内容（930）-Y
    up_time=1675674398

    params: typeCode :  : 跳转类型
    params: keyWord :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0正常
    params: msg : string : 描述
    params: data : array : 返回数据
              contentName : string : 跳转名称
              jumpContent : string : 跳转内容
              jumpType : number : 跳转类型
    """
    _method = "GET"
    _url = "/content/adv/jumpContent"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "typeCode": typeCode,  # 跳转类型
        "keyWord": keyWord,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/adv/detailConTentAdmin")
def content_adv_detailcontentadmin(current=None, orderByCommentCnt=None, essayKeyWords=None, size=None, headers=None, **kwargs):
    """
    点位内容-查询推荐页内容-Y
    up_time=1675673291

    params: current :  : 
    params: size :  : 
    params: essayKeyWords :  : 
    params: orderByCommentCnt :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              records : array : 
              total : string : 
              size : string : 
              current : string : 
    """
    _method = "GET"
    _url = "/content/adv/detailConTentAdmin"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,
        "size": size,
        "essayKeyWords": essayKeyWords,
        "orderByCommentCnt": orderByCommentCnt,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/adv/jumpTypeList")
def content_adv_jumptypelist( headers=None, **kwargs):
    """
    点位内容-查询跳转类型-Y
    up_time=1675674356

    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : array : 
              typeName : string : 跳转类型名称
              typeCode : string : 跳转类型编码
    """
    _method = "GET"
    _url = "/content/adv/jumpTypeList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/adv/cancelRecommend")
def content_adv_cancelrecommend(essayId=None, headers=None, **kwargs):
    """
    点位内容-取消推荐-Y
    up_time=1675673822

    params: essayId : string : 文章主键Id
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : string : 
    """
    _method = "POST"
    _url = "/content/adv/cancelRecommend"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "essayId": essayId,  # 文章主键Id
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/adv/detail")
def content_adv_detail(advPlaceId=None, headers=None, **kwargs):
    """
    点位-根据点位主键查询点位信息(930版本)
    up_time=1676685657

    params: advPlaceId :  : 广告点位主键 
 1:[发现-推荐]轮播图
 2:[发现-推荐]快捷入口
 5:[发现-资讯]金刚区
 6:[爱车]试驾页轮播
 8:[发现-推荐]精选内容
 9:[爱车-智能车控]
 10:[爱车-购车帮助]
 11:[我的-邀请好友]海报图
 12:[我的-积分]积分规则明细

    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : object : 
              records : object : 
    """
    _method = "GET"
    _url = "/content/adv/detail"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "advPlaceId": advPlaceId,  # 广告点位主键   1:[发现-推荐]轮播图  2:[发现-推荐]快捷入口  5:[发现-资讯]金刚区  6:[爱车]试驾页轮播  8:[发现-推荐]精选内容  9:[爱车-智能车控]  10:[爱车-购车帮助]  11:[我的-邀请好友]海报图  12:[我的-积分]积分规则明细 
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


