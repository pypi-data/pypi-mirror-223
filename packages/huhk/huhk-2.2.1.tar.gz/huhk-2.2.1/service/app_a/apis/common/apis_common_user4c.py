import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/common/user4C/queryActivitySource")
def common_user4c_queryactivitysource( headers=None, **kwargs):
    """
    用户列表-活动来源-Y
    up_time=1675305114

    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : array : 
              id : string : 例：抖音
              name : string : 例：抖音
    """
    _method = "GET"
    _url = "/common/user4C/queryActivitySource"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/common/user4C/page")
def common_user4c_page(lastLoginTimeEnd=None, userId=None, regisTimeBegin=None, userSystemSource=None, nickName=None, current=None, activitySource=None, status=None, mobile=None, createTimeEnd=None, memberSystemSource=None, createTimeStart=None, regisTimeEnd=None, ownerFlag=None, type=None, size=None, lastLoginTimeStart=None, headers=None, **kwargs):
    """
    用户列表-查询-Y
    up_time=1675318775

    params: userId :  : 用户Id
    params: mobile :  : 用户手机号码
    params: nickName :  : 用户昵称
    params: status :  : 会员状态 0：禁用 1：启用
    params: type :  : 用户类型 0：注册 1：非注册
    params: memberSystemSource :  : 会员来源系统： 1：APP、2：微信小程序、3：官网、4：H5
    params: size :  : 每页数据数
    params: current :  : 当前页数
    params: userSystemSource :  : 用户来源系统： 1：APP、2：微信小程序、3：官网、4：H5、5：SCRM、6：DMS
    params: activitySource :  : 用户活动来源 0：0元购、1：预约试驾、2：蓝牙共享车主、3：邀请好友、4：SCRM、5：DMS
    params: ownerFlag :  : 1：车主、2：使用人、3：共享车主、4：非车主；可多个标签叠加
    params: createTimeStart :  : 用户创建开始时间
    params: createTimeEnd :  : 用户创建结束时间
    params: regisTimeBegin :  : 会员注册开始时间
    params: regisTimeEnd :  : 会员注册结束时间
    params: lastLoginTimeStart :  : 用户最近登录开始时间
    params: lastLoginTimeEnd :  : 用户最近登录结束时间
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0：成功 1：失败
    params: msg : string :  信息 
    params: data : object : 数据
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
    _url = "/common/user4C/page"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户Id
        "mobile": mobile,  # 用户手机号码
        "nickName": nickName,  # 用户昵称
        "status": status,  # 会员状态 0：禁用 1：启用
        "type": type,  # 用户类型 0：注册 1：非注册
        "memberSystemSource": memberSystemSource,  # 会员来源系统： 1：APP、2：微信小程序、3：官网、4：H5
        "size": size,  # 每页数据数
        "current": current,  # 当前页数
        "userSystemSource": userSystemSource,  # 用户来源系统： 1：APP、2：微信小程序、3：官网、4：H5、5：SCRM、6：DMS
        "activitySource": activitySource,  # 用户活动来源 0：0元购、1：预约试驾、2：蓝牙共享车主、3：邀请好友、4：SCRM、5：DMS
        "ownerFlag": ownerFlag,  # 1：车主、2：使用人、3：共享车主、4：非车主；可多个标签叠加
        "createTimeStart": createTimeStart,  # 用户创建开始时间
        "createTimeEnd": createTimeEnd,  # 用户创建结束时间
        "regisTimeBegin": regisTimeBegin,  # 会员注册开始时间
        "regisTimeEnd": regisTimeEnd,  # 会员注册结束时间
        "lastLoginTimeStart": lastLoginTimeStart,  # 用户最近登录开始时间
        "lastLoginTimeEnd": lastLoginTimeEnd,  # 用户最近登录结束时间
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/common/user4C/vehicleInfo")
def common_user4c_vehicleinfo(mobile=None, userId=None, current=None, size=None, headers=None, **kwargs):
    """
    用户列表-详情-车辆信息-Y
    up_time=1675319192

    params: userId :  : 用户ID
    params: mobile :  : 用户手机号码
    params: current :  : 页码
    params: size :  : 每页大小
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0：成功 1：失败
    params: msg : string : 信息
    params: data : object : 数据
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
    _url = "/common/user4C/vehicleInfo"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
        "mobile": mobile,  # 用户手机号码
        "current": current,  # 页码
        "size": size,  # 每页大小
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/common/user4C/getById")
def common_user4c_getbyid(userId=None, headers=None, **kwargs):
    """
    用户中心-用户基本信息-Y
    up_time=1677207988

    params: userId :  : 用户主键
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0：成功 1：失败
    params: msg : string : 信息
    params: data : object : 数据
              userId : number : 用户Id
              avatarUrl : string : 头像URL
              realName : string : 真实姓名
              mobile : string : 用户号码
              sex : integer : 用户性别 用户性别 1:男生 2:女生 3:保密
              nickName : string : 昵称
              carAddress : string : 用车省市
              birthday : string : 用户生日
              explain : string : 说明简介
              owner : string : 车主身份
              wxOpenId : string : 微信openID
              appleId : string : appleID
              registerType : string : 注册来源
              userSystemSource : string : 用户来源系统
              externalCreateTime : string : 用户创建时间
              memberSystemSource : string : 会员来源系统
              createTime : string : 会员注册时间
              userTypeName : string : 0:注册 1 非注册   用户类型
              activitySource : string : 用户活动来源
              lastLoginTime : string : 最近登陆时间
              lastLoginClient : string : 最近登陆端
              historyLoginClient : string : 历史登陆端
              userPolicyCode : string : 用户协议版本号
              privacyPolicyCode : string : 隐私协议版本号
              userPolicySignTime : string : 用户协议签订时间
              privacyPolicySignTime : string : 隐私协议签订时间
              status : integer : 用户状态 是否可用 0：禁用 1：启用 - 列表页展示
              county : string : 用户区县
              city : string : 用户城市
              province : string : 用户省份
              usableQty : integer : 可用积分
              freezeQty : integer : 冻结积分
    """
    _method = "GET"
    _url = "/common/user4C/getById"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户主键
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/common/user4C/updateUser")
def common_user4c_updateuser(userId=None, headers=None, **kwargs):
    """
    用户中心-编辑官方账号-Y
    up_time=1675319403

    params: userId : text : Long；用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0 成功 1 失败
    params: msg : string : 信息
    params: data : boolean : 状态
    """
    _method = "POST"
    _url = "/common/user4C/updateUser"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # Long；用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/common/user4C/download")
def common_user4c_download(userIds=None, lastLoginTimeEnd=None, userId=None, regisTimeBegin=None, userSystemSource=None, downloadType=None, nickName=None, activitySource=None, status=None, mobile=None, createTimeEnd=None, memberSystemSource=None, createTimeStart=None, regisTimeEnd=None, ownerFlag=None, type=None, lastLoginTimeStart=None, headers=None, **kwargs):
    """
    用户列表-导出-Y
    up_time=1675148564

    params: userId :  : 用户Id
    params: mobile :  : 用户手机号
    params: nickName :  : 用户昵称
    params: status :  : 会员状态 0：禁用 1：启用
    params: type :  : 用户类型 0：注册 1：非注册
    params: memberSystemSource :  : 会员来源系统： 1：APP、2：微信小程序、3：官网、4：H5
    params: userSystemSource :  : 用户来源系统： 1：APP、2：微信小程序、3：官网、4：H5、5：SCRM、6：DMS
    params: activitySource :  : 用户活动来源 0：0元购、1：预约试驾、2：蓝牙共享车主、3：邀请好友、4：SCRM、5：DMS
    params: ownerFlag :  : 1：车主、2：使用人、3：共享车主、4：非车主；可多个标签叠加
    params: createTimeStart :  : 用户创建开始时间
    params: createTimeEnd :  : 用户创建结束时间
    params: regisTimeBegin :  : 会员注册开始时间
    params: regisTimeEnd :  : 会员注册结束时间
    params: lastLoginTimeStart :  : 会员最近登录开始时间
    params: lastLoginTimeEnd :  : 会员最近登录结束时间
    params: downloadType :  : 导出类型 1: 条件导出 2: 批量导出
    params: userIds :  : 导出用户主键集合，downloadType=2为必填
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/common/user4C/download"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户Id
        "mobile": mobile,  # 用户手机号
        "nickName": nickName,  # 用户昵称
        "status": status,  # 会员状态 0：禁用 1：启用
        "type": type,  # 用户类型 0：注册 1：非注册
        "memberSystemSource": memberSystemSource,  # 会员来源系统： 1：APP、2：微信小程序、3：官网、4：H5
        "userSystemSource": userSystemSource,  # 用户来源系统： 1：APP、2：微信小程序、3：官网、4：H5、5：SCRM、6：DMS
        "activitySource": activitySource,  # 用户活动来源 0：0元购、1：预约试驾、2：蓝牙共享车主、3：邀请好友、4：SCRM、5：DMS
        "ownerFlag": ownerFlag,  # 1：车主、2：使用人、3：共享车主、4：非车主；可多个标签叠加
        "createTimeStart": createTimeStart,  # 用户创建开始时间
        "createTimeEnd": createTimeEnd,  # 用户创建结束时间
        "regisTimeBegin": regisTimeBegin,  # 会员注册开始时间
        "regisTimeEnd": regisTimeEnd,  # 会员注册结束时间
        "lastLoginTimeStart": lastLoginTimeStart,  # 会员最近登录开始时间
        "lastLoginTimeEnd": lastLoginTimeEnd,  # 会员最近登录结束时间
        "downloadType": downloadType,  # 导出类型 1: 条件导出 2: 批量导出
        "userIds": userIds,  # 导出用户主键集合，downloadType=2为必填
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/common/user4C/beforePointsExport")
def common_user4c_beforepointsexport(userIds=None, lastLoginTimeEnd=None, userId=None, regisTimeBegin=None, userSystemSource=None, downloadType=None, nickName=None, activitySource=None, status=None, mobile=None, createTimeEnd=None, memberSystemSource=None, createTimeStart=None, regisTimeEnd=None, ownerFlag=None, type=None, lastLoginTimeStart=None, headers=None, **kwargs):
    """
    用户列表-导出前置判断-Y
    up_time=1675306476

    params: userId :  : 用户Id
    params: mobile :  : 用户手机号
    params: nickName :  : 用户昵称
    params: status :  : 账号状态 0：禁用 1：启用
    params: type :  : 用户类型 0：注册 1：非注册
    params: memberSystemSource :  : 用户来源系统： 1：APP、2：微信小程序、3：官网、4：H5
    params: userSystemSource :  : 用户来源系统： 1：APP、2：微信小程序、3：官网、4：H5、5：SCRM、6：DMS
    params: activitySource :  : 用户活动来源 0：0元购、1：预约试驾、2：蓝牙共享车主、3：邀请好友、4：SCRM、5：DMS
    params: ownerFlag :  :  1：车主、2：使用人、3：共享车主、4：非车主；可多个标签叠加
    params: createTimeStart :  : 用户创建开始时间
    params: createTimeEnd :  : 用户创建结束时间
    params: regisTimeBegin :  : 会员注册开始时间
    params: regisTimeEnd :  : 会员注册结束时间
    params: lastLoginTimeStart :  : 会员最近登录开始时间
    params: lastLoginTimeEnd :  : 会员最近登录结束时间
    params: downloadType :  : 1：条件导出 2：批量导出
    params: userIds :  : 用户Id downloadType为2时必填
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0：成功 1：失败
    params: msg : string : 描述
    params: data : boolean : true 调用参考导出条件搜索用户列表接口
    """
    _method = "GET"
    _url = "/common/user4C/beforePointsExport"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户Id
        "mobile": mobile,  # 用户手机号
        "nickName": nickName,  # 用户昵称
        "status": status,  # 账号状态 0：禁用 1：启用
        "type": type,  # 用户类型 0：注册 1：非注册
        "memberSystemSource": memberSystemSource,  # 用户来源系统： 1：APP、2：微信小程序、3：官网、4：H5
        "userSystemSource": userSystemSource,  # 用户来源系统： 1：APP、2：微信小程序、3：官网、4：H5、5：SCRM、6：DMS
        "activitySource": activitySource,  # 用户活动来源 0：0元购、1：预约试驾、2：蓝牙共享车主、3：邀请好友、4：SCRM、5：DMS
        "ownerFlag": ownerFlag,  #  1：车主、2：使用人、3：共享车主、4：非车主；可多个标签叠加
        "createTimeStart": createTimeStart,  # 用户创建开始时间
        "createTimeEnd": createTimeEnd,  # 用户创建结束时间
        "regisTimeBegin": regisTimeBegin,  # 会员注册开始时间
        "regisTimeEnd": regisTimeEnd,  # 会员注册结束时间
        "lastLoginTimeStart": lastLoginTimeStart,  # 会员最近登录开始时间
        "lastLoginTimeEnd": lastLoginTimeEnd,  # 会员最近登录结束时间
        "downloadType": downloadType,  # 1：条件导出 2：批量导出
        "userIds": userIds,  # 用户Id downloadType为2时必填
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/common/user4C/insert")
def common_user4c_insert(nickName=None, avatarUrl=None, explain=None, headers=None, **kwargs):
    """
    用户列表-新增-Y
    up_time=1675319481

    params: avatarUrl : text : String；图片地址
    params: explain : text : String；简介
    params: nickName : text : String；昵称
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0：成功 1：失败
    params: msg : string : 信息 
    params: data : boolean : TRUE：成功 FALSE：失败
    """
    _method = "POST"
    _url = "/common/user4C/insert"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "avatarUrl": avatarUrl,  # String；图片地址
        "explain": explain,  # String；简介
        "nickName": nickName,  # String；昵称
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/common/user4C/editStatus")
def common_user4c_editstatus(userId=None, status=None, headers=None, **kwargs):
    """
    用户中心-禁用/启用用户-Y
    up_time=1675320747

    params: userId : text : 
    params: status : number : 是否启用0：禁用 1：启用
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/common/user4C/editStatus"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,
        "status": status,  # 是否启用0：禁用 1：启用
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/common/user4C/auditExport")
def common_user4c_auditexport(userIds=None, userId=None, userLabel=None, downloadType=None, nickName=None, phone=None, registerType=None, ownerFlag=None, userType=None, headers=None, **kwargs):
    """
    导出用户审核列表-Y
    up_time=1675308559

    params: userId :  : 用户主键
    params: phone :  : 手机号
    params: nickName :  : 昵称
    params: ownerFlag :  : 是否车主认证1：是0：否
    params: userLabel :  : 用户标签
    params: registerType :  : 用户来源
    params: userType :  : 用户类型
    params: downloadType :  : 下载类型1：根据搜索条件导出2：多选导出
    params: userIds :  : 导出用户id集合，用英文,隔开
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/common/user4C/auditExport"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户主键
        "phone": phone,  # 手机号
        "nickName": nickName,  # 昵称
        "ownerFlag": ownerFlag,  # 是否车主认证1：是0：否
        "userLabel": userLabel,  # 用户标签
        "registerType": registerType,  # 用户来源
        "userType": userType,  # 用户类型
        "downloadType": downloadType,  # 下载类型1：根据搜索条件导出2：多选导出
        "userIds": userIds,  # 导出用户id集合，用英文,隔开
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/common/user4C/identity")
def common_user4c_identity(userId=None, headers=None, **kwargs):
    """
    根据id查询用户身份-Y
    up_time=1675319654

    params: userId :  : 用户主键
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : object : 
              records : object : 
    """
    _method = "GET"
    _url = "/common/user4C/identity"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户主键
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/common/user4C/updateAudit")
def common_user4c_updateaudit(userId=None, auditType=None, headers=None, **kwargs):
    """
    更新审核状态-Y
    up_time=1675319778

    params: userId : string : 用户ID
    params: auditType : integer : 认证类型（1：注销审核单据，2：车主认证审核单据）
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0：成功 1：失败
    params: msg : string : 信息
    params: data : boolean : 状态
    """
    _method = "POST"
    _url = "/common/user4C/updateAudit"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
        "auditType": auditType,  # 认证类型（1：注销审核单据，2：车主认证审核单据）
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/common/user4C/auditList")
def common_user4c_auditlist(userId=None, checkStatus=None, pageSize=None, nickName=None, pageNum=None, mobile=None, registerType=None, userName=None, headers=None, **kwargs):
    """
    根据用户审核状态搜索列表-Y
    up_time=1675320694

    params: userId :  : 用户id
    params: mobile :  : 手机号
    params: nickName :  : 用户昵称
    params: userName :  : 用户实名姓名
    params: registerType :  : 用户来源
    params: pageSize :  : 每页数量
    params: pageNum :  : 当前页数
    params: checkStatus :  : 状态 0-正常 1-审核中 2-通过3-审核不通过
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : object : 
              records : array : 
              auditedCount : number : 已通过数量
              auditCount : number : 待审核数量
              total : number : 
              size : number : 
              pages : number : 
              maxLimit : number : 待审核数据量
    """
    _method = "GET"
    _url = "/common/user4C/auditList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户id
        "mobile": mobile,  # 手机号
        "nickName": nickName,  # 用户昵称
        "userName": userName,  # 用户实名姓名
        "registerType": registerType,  # 用户来源
        "pageSize": pageSize,  # 每页数量
        "pageNum": pageNum,  # 当前页数
        "checkStatus": checkStatus,  # 状态 0-正常 1-审核中 2-通过3-审核不通过
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/common/user4C/getUserPoints")
def common_user4c_getuserpoints(userId=None, headers=None, **kwargs):
    """
    用户信息积分详情-？历史接口
    up_time=1676338919

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 永远成功
    params: msg : string : 信息
    params: data : object : 数据
              userPoints : object : 
              userPointsLog : array : 
    """
    _method = "GET"
    _url = "/common/user4C/getUserPoints"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


