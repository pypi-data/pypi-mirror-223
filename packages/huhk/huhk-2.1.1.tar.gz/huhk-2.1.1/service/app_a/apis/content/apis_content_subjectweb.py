import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/subjectweb/detailEssay")
def content_subjectweb_detailessay(current=None, subjectId=None, size=None, headers=None, **kwargs):
    """
    专题-后台官网专题文章列表-Y
    up_time=1675754018

    params: current :  : 当前页
    params: size :  : 当前条数
    params: subjectId :  : 专题主键id
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              records : array : 返回待发布的文章列表
              total : number : 总页数
              size : number : 每页大小
              current : number : 当前页
    """
    _method = "GET"
    _url = "/content/subjectweb/detailEssay"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,  # 当前页
        "size": size,  # 当前条数
        "subjectId": subjectId,  # 专题主键id
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/subjectweb/add")
def content_subjectweb_add(isService=None, isSearch=None, subPicUrl=None, subjectName=None, explain=None, parentId=None, web=None, status=None, level=None, siftFlag=None, recommend=None, serial=None, subjectRank=None, type=None, siftPicUrl=None, headers=None, **kwargs):
    """
    专题-后台官网专题新增-Y
    up_time=1675754357

    params: subjectName : string : 专题名称
    params: level : string : 专题等级
    params: status : string : 是否可用1：是 0：否
    params: explain : string : 说明
    params: type : string : 关联类型
    params: subPicUrl : string : 专题图片
    params: parentId : string : 父级专题主键
    params: serial : integer : 序号
    params: siftFlag : integer : 精选标识 0否 1是
    params: isService : integer : 是否有客服入口 0否 1是
    params: isSearch : integer : 是否配置搜索 0否 1是
    params: siftPicUrl : string : 精选配图
    params: web : string : 
    params: recommend : integer : 咨询页展示
    params: subjectRank : integer : 精选权重
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/subjectweb/add"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "subjectName": subjectName,  # 专题名称
        "level": level,  # 专题等级
        "status": status,  # 是否可用1：是 0：否
        "explain": explain,  # 说明
        "type": type,  # 关联类型
        "subPicUrl": subPicUrl,  # 专题图片
        "parentId": parentId,  # 父级专题主键
        "serial": serial,  # 序号
        "siftFlag": siftFlag,  # 精选标识 0否 1是
        "isService": isService,  # 是否有客服入口 0否 1是
        "isSearch": isSearch,  # 是否配置搜索 0否 1是
        "siftPicUrl": siftPicUrl,  # 精选配图
        "web": web,
        "recommend": recommend,  # 咨询页展示
        "subjectRank": subjectRank,  # 精选权重
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/subjectweb/treeList")
def content_subjectweb_treelist( headers=None, **kwargs):
    """
    专题-后台官网专题类型列表-Y
    up_time=1675756064

    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : array : 
              sub : array : 类目类型下的二级专题
              essList : array : 文章专题下的资讯分页
              childSubList : array : 类目类型下的二级专题
              jxJudge : number : 用于判定精选框 是否可以多选
    """
    _method = "GET"
    _url = "/content/subjectweb/treeList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/subjectweb/save")
def content_subjectweb_save(delFlag=None, isService=None, isSearch=None, subPicUrl=None, subjectName=None, explain=None, parentId=None, status=None, siftFlag=None, subjectId=None, type=None, headers=None, **kwargs):
    """
    专题-后台官网保存/更新-Y
    up_time=1675754842

    params: subjectId : string : 
    params: subjectName : string : 
    params: delFlag : string : 
    params: subPicUrl : string : 
    params: explain : string : 
    params: status : string : 
    params: type : string : 
    params: parentId : string : 
    params: siftFlag : string : 
    params: isService : string : 
    params: isSearch : string : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/subjectweb/save"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "subjectId": subjectId,
        "subjectName": subjectName,
        "delFlag": delFlag,
        "subPicUrl": subPicUrl,
        "explain": explain,
        "status": status,
        "type": type,
        "parentId": parentId,
        "siftFlag": siftFlag,
        "isService": isService,
        "isSearch": isSearch,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/subjectweb/del")
def content_subjectweb_del(subjectId=None, headers=None, **kwargs):
    """
    专题-后台官网删除专题-Y
    up_time=1675751503

    params: subjectId : string : 专题主键
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/subjectweb/del"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "subjectId": subjectId,  # 专题主键
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/subjectweb/detail")
def content_subjectweb_detail(subjectId=None, headers=None, **kwargs):
    """
    专题-后台官网查询专题详情-Y
    up_time=1675751256

    params: subjectId :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 已发布的文章列表
              subjectId : string : 专题主键
              subjectName : string : 专题名称
              level : number : 专题等级
              explain : string : 说明
              status : number : 是否可用：0.否1：是
              subPicUrl : null : 专题图片
              type : number : 专题类型1.类目专题 2.文章专题
              createTime : string : 创建时间
              userName : null : 维护人姓名
    """
    _method = "GET"
    _url = "/content/subjectweb/detail"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "subjectId": subjectId,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/subjectweb/detailEssayNew")
def content_subjectweb_detailessaynew(current=None, subjectId=None, size=None, headers=None, **kwargs):
    """
    新闻中心文章列表-Y
    up_time=1675753591

    params: current :  : 
    params: size :  : 
    params: subjectId :  : 2 官方新闻 3 自媒体 4 媒体报道  null 全部
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              records : array : 
              total : number : 总页数
              size : number : 每页大小
              curren : number : 当前页
    """
    _method = "GET"
    _url = "/content/subjectweb/detailEssayNew"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,
        "size": size,
        "subjectId": subjectId,  # 2 官方新闻 3 自媒体 4 媒体报道  null 全部
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


