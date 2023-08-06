import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/subject/detailEssay")
def content_subject_detailessay(subjectName=None, current=None, subjectId=None, size=None, headers=None, **kwargs):
    """
    专题-后台App专题文章列表-Y
    up_time=1675752193

    params: current :  : 
    params: size :  : 
    params: subjectId :  : Long
    params: subjectName :  :  string
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              records : array : 
              total : number : 总页数
              size : number : 每页大小
              current : number : 当前页
    """
    _method = "GET"
    _url = "/content/subject/detailEssay"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,
        "size": size,
        "subjectId": subjectId,  # Long
        "subjectName": subjectName,  #  string
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/subject/add")
def content_subject_add(subPicUrl=None, subjectName=None, parentId=None, explain=None, status=None, level=None, type=None, headers=None, **kwargs):
    """
    专题-后台App专题新增-Y
    up_time=1675749730

    params: subjectName : string : 专题名称
    params: parentId : string : 父级专题主键
    params: level : number : 专题等级
    params: status : number : 是否可用1：是0：否
    params: explain : string : 说明
    params: type : number : 关联类型
    params: subPicUrl : string : 专题图片
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/subject/add"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "subjectName": subjectName,  # 专题名称
        "parentId": parentId,  # 父级专题主键
        "level": level,  # 专题等级
        "status": status,  # 是否可用1：是0：否
        "explain": explain,  # 说明
        "type": type,  # 关联类型
        "subPicUrl": subPicUrl,  # 专题图片
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/subject/del")
def content_subject_del(subjectId=None, headers=None, **kwargs):
    """
    专题-后台App删除专题-Y
    up_time=1675749831

    params: subjectId : text : 
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/subject/del"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "subjectId": subjectId,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/subject/mobileSubject")
def content_subject_mobilesubject(serial=None, parentId=None, subjectId=None, headers=None, **kwargs):
    """
    专题-后台App移动专题更新-Y
    up_time=1675750974

    params: subjectId : text : 移动的专题ID
    params: parentId : text : 移动到的一级专题ID
    params: serial : text : 排序
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功
    params: msg : string : 描述
    params: data : boolean : true成功
    """
    _method = "POST"
    _url = "/content/subject/mobileSubject"

    _headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    _headers.update({"headers": headers})

    _data = {
        "subjectId": subjectId,  # 移动的专题ID
        "parentId": parentId,  # 移动到的一级专题ID
        "serial": serial,  # 排序
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/subject/getEssaySubjects")
def content_subject_getessaysubjects( headers=None, **kwargs):
    """
    文章-发布到下拉数据-Y
    up_time=1675750961

    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : array : 
              subjectId : string : 专题编码
              subjectName : string : 专题名称
              level : number : 级别
              parentId : ['string', 'null'] : 上级专题编码
              explain : null : 
              status : number : 
              subPicUrl : ['string', 'null'] : 
              type : number : 
              serial : number : 
              createTime : string : 
              createBy : null : 
              updateTime : string : 
              updateBy : null : 
              delFlag : number : 
    """
    _method = "GET"
    _url = "/content/subject/getEssaySubjects"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/subject/detail")
def content_subject_detail(subjectId=None, headers=None, **kwargs):
    """
    专题-后台App查询专题详情-Y
    up_time=1675752083

    params: subjectId :  : 广告位主键
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : object : 
              subjectId : number : 专题主键
              subjectName : string : 专题名称
              level : number : 专题等级
              parentId : number : 上级主题ID
              serial : integer : 序号
              createTime : string : 创建时间
              createBy : number : 创建人
              updateTime : string : 更新时间
              updateBy : number : 更新人
              delFlag : integer : 标记：0.正常 1.删除
              subPicUrl : string : 专题图片
              essayList : array : 文章列表
              type : number : 专题类型1.类目专题 2.文章专题
              userName : string : 维护人姓名
    """
    _method = "GET"
    _url = "/content/subject/detail"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "subjectId": subjectId,  # 广告位主键
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/subject/treeList")
def content_subject_treelist( headers=None, **kwargs):
    """
    专题-后台APP专题类型列表-Y
    up_time=1675749366

    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : object : 
              records : array : 
    """
    _method = "GET"
    _url = "/content/subject/treeList"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/subject/save")
def content_subject_save(delFlag=None, isService=None, isSearch=None, subPicUrl=None, subjectName=None, explain=None, parentId=None, status=None, level=None, siftFlag=None, subjectId=None, type=None, headers=None, **kwargs):
    """
    专题-后台App保存/更新-Y
    up_time=1675749773

    params: subjectId : number : 
    params: subjectName : string : 
    params: level : number : 
    params: delFlag : number : 
    params: subPicUrl : string : 
    params: explain : string : 
    params: status : number : 
    params: type : number : 
    params: parentId : string : 父ID
    params: siftFlag : number : 是否精选 1是 0否
    params: isService : number : 是否设置客服入口 1是 0否
    params: isSearch : number : 是否配置搜索 0否 1是
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/subject/save"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "subjectId": subjectId,
        "subjectName": subjectName,
        "level": level,
        "delFlag": delFlag,
        "subPicUrl": subPicUrl,
        "explain": explain,
        "status": status,
        "type": type,
        "parentId": parentId,  # 父ID
        "siftFlag": siftFlag,  # 是否精选 1是 0否
        "isService": isService,  # 是否设置客服入口 1是 0否
        "isSearch": isSearch,  # 是否配置搜索 0否 1是
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


