import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/agreement/getAgreement")
def content_agreement_getagreement( headers=None, **kwargs):
    """
    查询创建活动所需协议
    up_time=1678259215

    params: headers : 请求头
    ====================返回======================
    params: code : string : 
    params: msg : string : 
    params: data : array : 
              agreementId : string : 协议id
              code : string : 协议编码
              name : string : 协议名称
              content : string : 协议正文
              updateTime : string : data更新时间
              updateBy : number : 更新人
              updateByName : string : 更新人名称
              status : integer : 1.生效 2.过期
              version : string : 版本号
              createTime : string : data发布日期
              enableTime : string : data生效日期
    """
    _method = "GET"
    _url = "/content/agreement/getAgreement"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/agreement/getByCode")
def content_agreement_getbycode(agreementCode=None, headers=None, **kwargs):
    """
    协议-C端用户根据编码查询协议-Y
    up_time=1675217511

    params: agreementCode :  : PRIVACYPOLICY:隐私协议，USERPOLICY：用户协议， THIRDPARTYSDKPOLICY：第三方sdk目录，POINTRULE：积分规则，SIGININRULE：签到规则
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              agreementId : string : 协议id
              code : string : 协议编码
              name : string : 协议名称
              content : string : 协议内容
              updateTime : string : 修改时间
              updateBy : string : 修改人
              updateByName : string : 修改人姓名
              status : number : 状态
              version : string : 协议版本
              createTime : string : 创建实际
              enableTime : string : 启用时间
    """
    _method = "GET"
    _url = "/content/agreement/getByCode"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "agreementCode": agreementCode,  # PRIVACYPOLICY:隐私协议，USERPOLICY：用户协议， THIRDPARTYSDKPOLICY：第三方sdk目录，POINTRULE：积分规则，SIGININRULE：签到规则
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/agreement/getAgreementByCode")
def content_agreement_getagreementbycode(agreementCode=None, headers=None, **kwargs):
    """
    协议-h5查询协议-Y
    up_time=1675680320

    params: agreementCode :  : 协议编码 
隐私协议:PRIVACYPOLICY、
用户协议:USERPOLICY、
权限清单:PERMISSIONSLIST、
第三方SDK列表:THIRDPARTYSDKPOLICY、
用户注销: USERDESTROY
车机服务协议: CARSERVICE
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              agreementId : string : 协议主键
              code : string : 协议编码
              name : string : 协议名称
              content : string : 协议内容
              updateTime : string : 更新时间
              updateBy : string : 更新人
              updateByName : null : 更新人名称
              status : number : 
              version : string : 1.生效 2.过期
              createTime : null : 创建日期
              enableTime : null : 生效日期
    """
    _method = "GET"
    _url = "/content/agreement/getAgreementByCode"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "agreementCode": agreementCode,  # 协议编码  隐私协议:PRIVACYPOLICY、 用户协议:USERPOLICY、 权限清单:PERMISSIONSLIST、 第三方SDK列表:THIRDPARTYSDKPOLICY、 用户注销: USERDESTROY 车机服务协议: CARSERVICE
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/agreement/updateStatus")
def content_agreement_updatestatus(agreementId=None, status=None, code=None, headers=None, **kwargs):
    """
    协议-停用启用协议-Y
    up_time=1675680241

    params: agreementId : text : 
    params: status : text : 状态 1 启用 2 停用
    params: code : text : 协议编码
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/agreement/updateStatus"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "agreementId": agreementId,
        "status": status,  # 状态 1 启用 2 停用
        "code": code,  # 协议编码
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/agreement/list")
def content_agreement_list(current=None, size=None, headers=None, **kwargs):
    """
    协议-协议列表-Y
    up_time=1678246318

    params: size :  : 每页数据数
    params: current :  : 当前页
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : array : 
              agreementId : string : 协议id
              name : string : 协议名称
              code : string : 协议编码
              content : string : 协议内容
              updateTime : string : 更新时间
              updateBy : string : 更新人id
              updateByName : string : 更新人名称
              status : number : 1.生效 2.过期
              version : string : 版本号
              createTime : string : 发布时间
              enableTime : string : 生效时间
    """
    _method = "GET"
    _url = "/content/agreement/list"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "size": size,  # 每页数据数
        "current": current,  # 当前页
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/agreement/save")
def content_agreement_save(content=None, version=None, name=None, code=None, headers=None, **kwargs):
    """
    协议-新增协议-Y
    up_time=1675675877

    params: name : string : 协议名
    params: content : string : 内容
    params: version : number : 版本号
    params: code : string : 协议编码
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/agreement/save"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "name": name,  # 协议名
        "content": content,  # 内容
        "version": version,  # 版本号
        "code": code,  # 协议编码
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/agreement/update")
def content_agreement_update(content=None, version=None, code=None, agreementId=None, name=None, headers=None, **kwargs):
    """
    协议-更新协议-Y
    up_time=1675680222

    params: name : string : 协议名
    params: content : string : 内容
    params: version : number : 版本号
    params: agreementId : string : 协议id
    params: code : string : 协议编码
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/agreement/update"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "name": name,  # 协议名
        "content": content,  # 内容
        "version": version,  # 版本号
        "agreementId": agreementId,  # 协议id
        "code": code,  # 协议编码
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/agreement/getById")
def content_agreement_getbyid(agreementId=None, headers=None, **kwargs):
    """
    协议-根据id获取详情-Y
    up_time=1675680268

    params: agreementId :  : 协议主键1-隐私协议2-用户协议3-第三方SDK目录
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : object : 
              agreementId : number : 协议主键
              name : string : 协议名称
              code : string : 协议编码
              content : string : 协议内容
    """
    _method = "GET"
    _url = "/content/agreement/getById"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "agreementId": agreementId,  # 协议主键1-隐私协议2-用户协议3-第三方SDK目录
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


