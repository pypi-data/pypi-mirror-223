import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/content/hotSearch/rank")
def content_hotsearch_rank(kId=None, rank=None, headers=None, **kwargs):
    """
    热门搜索-修改权重-Y
    up_time=1675737497

    params: kId : string : 主键id
    params: rank : string : 权重
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0 成功 1失败
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/hotSearch/rank"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "kId": kId,  # 主键id
        "rank": rank,  # 权重
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/hotSearch/list")
def content_hotsearch_list(kId=None, rank=None, headers=None, **kwargs):
    """
    热门搜索-列表-Y
    up_time=1675737340

    params: kId : string : 主键id
    params: rank : string : 权重
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              records : array : 
              total : number : 
              size : number : 
              current : number : 
              pages : number : 
    """
    _method = "GET"
    _url = "/content/hotSearch/list"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "kId": kId,  # 主键id
        "rank": rank,  # 权重
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/content/hotSearch/insert")
def content_hotsearch_insert(keyWord=None, point=None, headers=None, **kwargs):
    """
    热门搜索-新增-Y
    up_time=1675737410

    params: keyWord : string : 关键词(城市名)
    params: point : string : 1 发现-搜索 4 活动定位
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0 成功  1 失败
    params: msg : string : 
    params: data : boolean : 
    """
    _method = "POST"
    _url = "/content/hotSearch/insert"

    _headers = {
        "Content-Type": "application/json",
    }
    _headers.update({"headers": headers})

    _data = {
        "keyWord": keyWord,  # 关键词(城市名)
        "point": point,  # 1 发现-搜索 4 活动定位
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


