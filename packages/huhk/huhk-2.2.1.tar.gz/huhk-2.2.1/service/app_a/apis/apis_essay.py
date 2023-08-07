import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/essay/batch")
def essay_batch(essayId=None, batchType=None, headers=None, **kwargs):
    """
    文章-批量操作-Y
    up_time=1675736143

    params: essayId :  : 文章主键
    params: batchType :  : 1：归档2：撤回3：置顶4：取消置顶
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : null : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/essay/batch"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "essayId": essayId,  # 文章主键
        "batchType": batchType,  # 1：归档2：撤回3：置顶4：取消置顶
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/essay/queryListCount")
def essay_querylistcount(author=None, status=None, essayId=None, keyWord=None, subjectId=None, startTime=None, endTime=None, headers=None, **kwargs):
    """
    文章-获取列表状态数量-Y
    up_time=1675736107

    params: essayId :  : 文章主键
    params: keyWord :  : 搜索关键字
    params: author :  : 作者
    params: startTime :  : 搜索起始时间
    params: endTime :  : 搜索结束时间
    params: subjectId :  : 专题主键
    params: status :  : 状态
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              toAuditCount : number : 待审核文章数量
              releasedCount : number : 已发布文章数量（预留）
    """
    _method = "GET"
    _url = "/essay/queryListCount"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "essayId": essayId,  # 文章主键
        "keyWord": keyWord,  # 搜索关键字
        "author": author,  # 作者
        "startTime": startTime,  # 搜索起始时间
        "endTime": endTime,  # 搜索结束时间
        "subjectId": subjectId,  # 专题主键
        "status": status,  # 状态
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


