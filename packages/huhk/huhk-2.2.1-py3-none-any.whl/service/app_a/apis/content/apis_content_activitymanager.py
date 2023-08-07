import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/activityManager/updatePerson")
def content_activitymanager_updateperson(needLimitPeople=None, activityId=None, limitPeople=None, headers=None, **kwargs):
    """
    活动 -修改报名人数(930)-Y
    up_time=1675238032

    params: activityId : string : 活动Id
    params: needLimitPeople : string : 是否限制 0 不限制 1限制
    params: limitPeople : number : 限制人数
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/activityManager/updatePerson"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "activityId": activityId,  # 活动Id
        "needLimitPeople": needLimitPeople,  # 是否限制 0 不限制 1限制
        "limitPeople": limitPeople,  # 限制人数
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/activityManager/updateEnrollTime")
def content_activitymanager_updateenrolltime(activityId=None, enrollStartTime=None, enrollTime=None, headers=None, **kwargs):
    """
    活动 -修改报名时间-Y
    up_time=1675238090

    params: activityId : string : 活动Id
    params: enrollStartTime : string : 报名开始时间
    params: enrollTime : string : 报名结束时间
    params: headers : 请求头
    ====================返回======================
    params: code : number : 编码
    params: msg : string : 信息
    params: data : boolean : 数据
    """
    _method = "POST"
    _url = "/content/activityManager/updateEnrollTime"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "activityId": activityId,  # 活动Id
        "enrollStartTime": enrollStartTime,  # 报名开始时间
        "enrollTime": enrollTime,  # 报名结束时间
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/activityManager/page")
def content_activitymanager_page(activityTimeSort=None, title=None, pushTimeSort=None, beginTime=None, status=None, province=None, createTimeSort=None, city=None, target=None, endTime=None, activityId=None, headers=None, **kwargs):
    """
    活动列表查询（930版本）-Y
    up_time=1675147665

    params: activityId :  : 
    params: title :  : 
    params: beginTime :  : 2022-01-18 00:00:00 （一定要带上00:00:00）
    params: endTime :  : 2022-01-18 23:59:59 （一定要带上23:59:59）
    params: target :  : 1：全部用户,2：车主用户,3：非车主用户,4:使用人,5：车主&使用人,6：非车主&非使用人
    params: status :  : 活动状态: 不传查全部， 2.待审核  4.待发布 5.已发布 6.审核不过 7.已撤回 8.已归档 9.停止报名 10.已结束 11.已下架  ；查询时候传的状态：12.已删除
    params: province :  : 省（编码 areaId）全国则不需要传值
    params: city :  : 市（编码areaId）
    params: createTimeSort :  : 创建时间排序（DESC（倒序））|ASC（正序））
    params: activityTimeSort :  : 活动时间排序（DESC|ASC）
    params: pushTimeSort :  : 发布时间排序（DESC|ASC）
    params: headers : 请求头
    ====================返回======================
    params: code : number : 接口状态
    params: msg : string : 提示信息
    params: data : object : 
              records : array : 
              total : number : 总数量
              pageSize : number : 分页大小
              pageNum : number : 当前页码
              pages : number : 总页数
              nextPage : number : 下一页
              size : number : 当前页的数量
              proPage : number : 上一页
              checkWaitStatusCount : number : 待审核数量
              publishWaitStatusCount : number : 待发布数量
    """
    _method = "GET"
    _url = "/content/activityManager/page"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "activityId": activityId,
        "title": title,
        "beginTime": beginTime,  # 2022-01-18 00:00:00 （一定要带上00:00:00）
        "endTime": endTime,  # 2022-01-18 23:59:59 （一定要带上23:59:59）
        "target": target,  # 1：全部用户,2：车主用户,3：非车主用户,4:使用人,5：车主&使用人,6：非车主&非使用人
        "status": status,  # 活动状态: 不传查全部， 2.待审核  4.待发布 5.已发布 6.审核不过 7.已撤回 8.已归档 9.停止报名 10.已结束 11.已下架  ；查询时候传的状态：12.已删除
        "province": province,  # 省（编码 areaId）全国则不需要传值
        "city": city,  # 市（编码areaId）
        "createTimeSort": createTimeSort,  # 创建时间排序（DESC（倒序））|ASC（正序））
        "activityTimeSort": activityTimeSort,  # 活动时间排序（DESC|ASC）
        "pushTimeSort": pushTimeSort,  # 发布时间排序（DESC|ASC）
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/activityManager/actInfoUpdate")
def content_activitymanager_actinfoupdate(operationType=None, activityId=None, headers=None, **kwargs):
    """
    活动操作停止报名和结束活动-Y
    up_time=1675393449

    params: activityId : text : 活动ID
    params: operationType : text : 1停止报名 2活动结束
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功
    params: msg : string : 描述
    params: data : boolean : true成功
    """
    _method = "POST"
    _url = "/content/activityManager/actInfoUpdate"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "activityId": activityId,  # 活动ID
        "operationType": operationType,  # 1停止报名 2活动结束
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/activityManager/setActivitySort")
def content_activitymanager_setactivitysort(activityId=None, sort=None, headers=None, **kwargs):
    """
    设置活动权重(930版本)-Y
    up_time=1675237750

    params: activityId : string : 活动Id
    params: sort : number : 权重
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/activityManager/setActivitySort"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "activityId": activityId,  # 活动Id
        "sort": sort,  # 权重
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/activityManager/getActivityInfo/")
def content_activitymanager_getactivityinfo_(activityId=None, headers=None, **kwargs):
    """
    获取活动详情-Y
    up_time=1678256790

    params: activityId :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              activityId : string : 活动ID
              createTime : string : 创建时间
              createBy : string : 创建人
              createByName : ['string', 'null'] : 创建人名称
              mobile : ['string', 'null'] : 手机号
              avatar : ['string', 'null'] : 头像
              username : ['string', 'null'] : 用户名称
              userType : ['number', 'null'] : 用户类型：2：内部用户3：虚拟用户
              activityPicUrl : ['string', 'null'] : 活动封面图
              title : string : 标题
              joinCnt : string : 参加人数
              activityJoinList : array : 活动参与人数数据集合
              content : string : 活动简介
              beginTime : string : 开始时间
              endTime : string : 结束时间
              needArea : string : 需要区域：0不需要 1需要
              province : ['null', 'string'] : 省
              city : ['null', 'string'] : 市
              county : ['null', 'string'] : 区
              activityAddr : string : 活动地址
              reason : string : 原因
              publishType : integer : 
              status : number : 状态: 1.新建 2.待审核 3.审核通过 4.待发布 5.已发布 6.审核不过  7.已撤回 8.已归档；查询时候传的状态：9.停止报名 10.已结束
              statusName : ['string', 'null'] : 状态名称
              authId : number : 作者ID
              enrollStartTime : string : 报名开始时间
              enrollTime : string : 报名截止时间
              needLimitPeople : string : 需要人数限制（活动人数）：0不需要 1需要
              limitPeople : integer : 人数限制
              customerGroup : string : 参与对象（1：全部用户，2：车主用户，3：非车主用户）
     * 1：全部用户,2：车主用户,3：非车主用户,4:使用人,5：车主&使用人,6：非车主&非使用人
              checkTime : string : 审核时间
              publishTime : string : 发布时间
              topFlag : integer : 置顶
              sort : integer : 权重
              activityCreateUser : string : 活动创建者ID
              agreementId : string : 协议id
              agreementName : string : 协议名称
              agreementCode : string : 协议编码
    """
    _method = "GET"
    _url = "/content/activityManager/getActivityInfo/{activityId}"
    _url = get_url(_url, locals())

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
        "activityId": activityId,
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/activityManager/activityTop/")
def content_activitymanager_activitytop_(activityId=None, topFlag=None, headers=None, **kwargs):
    """
    活动置顶/取消置顶-Y
    up_time=1675238359

    params: activityId : text : 活动ID
    params: topFlag : text : 0不置顶  1置顶
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/activityManager/activityTop/"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "activityId": activityId,  # 活动ID
        "topFlag": topFlag,  # 0不置顶  1置顶
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/activityManager/activityJoinUserExport")
def content_activitymanager_activityjoinuserexport(activityId=None, headers=None, **kwargs):
    """
    活动报名用户数据导出-Y
    up_time=1675238544

    params: activityId :  : 活动Id
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/content/activityManager/activityJoinUserExport"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "activityId": activityId,  # 活动Id
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/activityManager/save")
def content_activitymanager_save(title=None, publishType=None, authId=None, coordinate=None, county=None, activityPicUrl=None, status=None, province=None, publishTime=None, needLimitPeople=None, content=None, reason=None, activityId=None, enrollTime=None, activityAddr=None, city=None, agreementId=None, activityPicURL=None, needArea=None, beginTime=None, customerGroup=None, endTime=None, enrollStartTime=None, limitPeople=None, headers=None, **kwargs):
    """
    活动新增-Y
    up_time=1678257957

    params: activityId : text : 
    params: title : text : 
    params: reason : text : 
    params: activityPicUrl : text : 
    params: beginTime : text : 
    params: endTime : text : 汉字
    params: needArea : text : 汉字
    params: province : text : 汉字
    params: city : text : 34.232342,112.342345
    params: county : text : 
    params: coordinate : text : 
    params: needLimitPeople : text : 
    params: limitPeople : text : 
    params: enrollStartTime : text : 
    params: enrollTime : text : 
    params: publishType : text : 地图获取
    params: publishTime : text : 
    params: content : text : 
    params: authId : text : 
    params: status : text : 
    params: activityAddr : text : 
    params: customerGroup : text : 
    params: activityPicURL : string : 活动封面图
    params: agreementId : number : 协议ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/activityManager/save"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "activityId": activityId,
        "title": title,
        "reason": reason,
        "activityPicUrl": activityPicUrl,
        "beginTime": beginTime,
        "endTime": endTime,  # 汉字
        "needArea": needArea,  # 汉字
        "province": province,  # 汉字
        "city": city,  # 34.232342,112.342345
        "county": county,
        "coordinate": coordinate,
        "needLimitPeople": needLimitPeople,
        "limitPeople": limitPeople,
        "enrollStartTime": enrollStartTime,
        "enrollTime": enrollTime,
        "publishType": publishType,  # 地图获取
        "publishTime": publishTime,
        "content": content,
        "authId": authId,
        "status": status,
        "activityAddr": activityAddr,
        "customerGroup": customerGroup,
        "activityPicURL": activityPicURL,  # 活动封面图
        "agreementId": agreementId,  # 协议ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/activityManager/update")
def content_activitymanager_update(title=None, publishType=None, authId=None, coordinate=None, county=None, activityPicUrl=None, status=None, province=None, publishTime=None, content=None, needLimitPeople=None, reason=None, activityId=None, enrollTime=None, activityAddr=None, city=None, activityPicURL=None, needArea=None, beginTime=None, customerGroup=None, endTime=None, enrollStartTime=None, limitPeople=None, headers=None, **kwargs):
    """
    活动编辑（930版本）-Y
    up_time=1675237616

    params: activityId : text : 
    params: title : text : 
    params: reason : text : 
    params: activityPicUrl : text : 
    params: beginTime : text : 
    params: endTime : text : 
    params: province : text : 汉字
    params: city : text : 汉字
    params: county : text : 
    params: coordinate : text : 34.232342,112.342345
    params: limitPeople : text : 
    params: enrollTime : text : 
    params: publishType : text : 
    params: publishTime : text : 
    params: content : text : 
    params: authId : text : 
    params: activityPicURL : string : 活动封面图
    params: needArea : string : 是否需要区域
    params: needLimitPeople : string : 是否需要人数限制
    params: enrollStartTime : string : 报名开始时间
    params: status : integer : 活动状态: 不传查全部
     * 2:待审核
     * 3:审核通过
     * 4:待上架
     * 5:已上架
     * 6:审核不通过
     * 9:停止报名
     * 10:已结束
     * 11:已下架
     * 12:已删除
    params: activityAddr : string : 活动地址
    params: customerGroup : string : 参与对象（1：全部用户，2：车主用户，3：非车主用户）
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/activityManager/update"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "activityId": activityId,
        "title": title,
        "reason": reason,
        "activityPicUrl": activityPicUrl,
        "beginTime": beginTime,
        "endTime": endTime,
        "province": province,  # 汉字
        "city": city,  # 汉字
        "county": county,
        "coordinate": coordinate,  # 34.232342,112.342345
        "limitPeople": limitPeople,
        "enrollTime": enrollTime,
        "publishType": publishType,
        "publishTime": publishTime,
        "content": content,
        "authId": authId,
        "activityPicURL": activityPicURL,  # 活动封面图
        "needArea": needArea,  # 是否需要区域
        "needLimitPeople": needLimitPeople,  # 是否需要人数限制
        "enrollStartTime": enrollStartTime,  # 报名开始时间
        "status": status,  # 活动状态: 不传查全部      * 2:待审核      * 3:审核通过      * 4:待上架      * 5:已上架      * 6:审核不通过      * 9:停止报名      * 10:已结束      * 11:已下架      * 12:已删除
        "activityAddr": activityAddr,  # 活动地址
        "customerGroup": customerGroup,  # 参与对象（1：全部用户，2：车主用户，3：非车主用户）
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/activityManager/publishUpdate")
def content_activitymanager_publishupdate(activityId=None, activityIds=None, publishStatus=None, status=None, headers=None, **kwargs):
    """
    活动发布状态修改(930)-Y
    up_time=1675392693

    params: activityIds : text : 单个记录修改传["xxxxx"]
    params: publishStatus : text : 
    params: activityId : string : 活动Id
    params: status : number : //状态: 1.新建 2.待审核 3.审核通过 4.待发布 5.已发布 6.审核不过 7.已撤回 8.已归档 9.停止报名 10.已结束 11.已下架；查询时候传的状态：12.已删除
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/activityManager/publishUpdate"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "activityIds": activityIds,  # 单个记录修改传["xxxxx"]
        "publishStatus": publishStatus,
        "activityId": activityId,  # 活动Id
        "status": status,  # //状态: 1.新建 2.待审核 3.审核通过 4.待发布 5.已发布 6.审核不过 7.已撤回 8.已归档 9.停止报名 10.已结束 11.已下架；查询时候传的状态：12.已删除
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/activityManager/statusUpdate")
def content_activitymanager_statusupdate(checkStatus=None, activityIds=None, headers=None, **kwargs):
    """
    活动审核状态修改-Y
    up_time=1675392843

    params: checkStatus : text : 
    params: activityIds : array : 活动IDs
              type : string : None
    params: headers : 请求头
    ====================返回======================
    params: code : string : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/activityManager/statusUpdate"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "checkStatus": checkStatus,
        "activityIds": activityIds,  # 活动IDs
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/activityManager/enrollUpdate")
def content_activitymanager_enrollupdate(checkEnroll=None, activityIds=None, headers=None, **kwargs):
    """
    活动报名状态修改-Y
    up_time=1675393335

    params: activityIds : text : 单个记录修改传["xxxxx"]
    params: checkEnroll : text : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/activityManager/enrollUpdate"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "activityIds": activityIds,  # 单个记录修改传["xxxxx"]
        "checkEnroll": checkEnroll,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/activityManager/activityExport")
def content_activitymanager_activityexport(activityTimeSort=None, title=None, pushTimeSort=None, beginTime=None, status=None, province=None, createTimeSort=None, city=None, target=None, endTime=None, activityId=None, headers=None, **kwargs):
    """
    活动数据导出-Y
    up_time=1675149098

    params: activityId :  : 
    params: title :  : 
    params: beginTime :  : 2022-01-18 00:00:00 （一定要带上00:00:00）
    params: endTime :  : 2022-01-18 23:59:59 （一定要带上23:59:59）
    params: target :  : 1：全部用户,2：车主用户,3：非车主用户,4:使用人,5：车主&使用人,6：非车主&非使用人
    params: status :  : 活动状态: 不传查全部， 2.待审核  4.待发布 5.已发布 6.审核不过 7.已撤回 8.已归档 9.停止报名 10.已结束 11.已下架  ；查询时候传的状态：12.已删除
    params: province :  : 省（编码 areaId）全国则不需要传值
    params: city :  : 市（编码areaId）
    params: createTimeSort :  : 创建时间排序（DESC（倒序））|ASC（正序））
    params: activityTimeSort :  : 活动时间排序（DESC|ASC）
    params: pushTimeSort :  : 发布时间排序（DESC|ASC）
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/content/activityManager/activityExport"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "activityId": activityId,
        "title": title,
        "beginTime": beginTime,  # 2022-01-18 00:00:00 （一定要带上00:00:00）
        "endTime": endTime,  # 2022-01-18 23:59:59 （一定要带上23:59:59）
        "target": target,  # 1：全部用户,2：车主用户,3：非车主用户,4:使用人,5：车主&使用人,6：非车主&非使用人
        "status": status,  # 活动状态: 不传查全部， 2.待审核  4.待发布 5.已发布 6.审核不过 7.已撤回 8.已归档 9.停止报名 10.已结束 11.已下架  ；查询时候传的状态：12.已删除
        "province": province,  # 省（编码 areaId）全国则不需要传值
        "city": city,  # 市（编码areaId）
        "createTimeSort": createTimeSort,  # 创建时间排序（DESC（倒序））|ASC（正序））
        "activityTimeSort": activityTimeSort,  # 活动时间排序（DESC|ASC）
        "pushTimeSort": pushTimeSort,  # 发布时间排序（DESC|ASC）
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/activityManager/listLog")
def content_activitymanager_listlog(activityId=None, headers=None, **kwargs):
    """
    活动状态流程-Y
    up_time=1675648649

    params: activityId :  : 活动id
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : array : 
              activityLogId : number : 日志主键
              activityId : string : 活动主键
              lastStatus : string : 之前的状态
              lastStatusName : integer : 之前的状态名称
              currentStatus : integer : 当前状态
              currentStatusName : string : 当前状态名称
              userId : number : 用户ID
              userName : string : 用户名称
              time : string : 时间
              reason : string : 原因
    """
    _method = "GET"
    _url = "/content/activityManager/listLog"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "activityId": activityId,  # 活动id
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


