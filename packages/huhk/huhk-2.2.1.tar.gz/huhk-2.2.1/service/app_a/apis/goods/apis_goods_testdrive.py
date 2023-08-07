import allure

from service.app_a import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/goods/testDrive/driveExports")
def goods_testdrive_driveexports(shopName=None, testDriveIdStr=None, channel=None, exportType=None, mobile=None, startTime=None, endTime=None, userName=None, headers=None, **kwargs):
    """
    试驾列表文件导出接口-Y
    up_time=1675390810

    params: mobile :  : 手机号
    params: userName :  : 用户名
    params: shopName :  : 店名
    params: channel :  : 渠道
    params: startTime :  : 开始时间
    params: endTime :  : 结束时间
    params: exportType :  : 导出类型
    params: testDriveIdStr :  : 订单集合字符串
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/goods/testDrive/driveExports"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "mobile": mobile,  # 手机号
        "userName": userName,  # 用户名
        "shopName": shopName,  # 店名
        "channel": channel,  # 渠道
        "startTime": startTime,  # 开始时间
        "endTime": endTime,  # 结束时间
        "exportType": exportType,  # 导出类型
        "testDriveIdStr": testDriveIdStr,  # 订单集合字符串
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/goods/testDrive/page")
def goods_testdrive_page(shopName=None, pageSize=None, channel=None, pageNum=None, mobile=None, startTime=None, endTime=None, userName=None, headers=None, **kwargs):
    """
    试驾查询接口-Y
    up_time=1675390631

    params: mobile :  : 手机号
    params: userName :  : 客户名
    params: shopName :  : 店名
    params: channel :  : 渠道
    params: startTime :  : 开始时间
    params: endTime :  : 结束时间
    params: pageNum :  : 当前页数
    params: pageSize :  : 每页数据数
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0-成功；1-失败
    params: msg : string : 信息
    params: data : object : 数据
              records : array : 
              total : string : 总数量
              size : string : 分页大小
              current : string : 当前页码
              pages : string : 总页数
    """
    _method = "GET"
    _url = "/goods/testDrive/page"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "mobile": mobile,  # 手机号
        "userName": userName,  # 客户名
        "shopName": shopName,  # 店名
        "channel": channel,  # 渠道
        "startTime": startTime,  # 开始时间
        "endTime": endTime,  # 结束时间
        "pageNum": pageNum,  # 当前页数
        "pageSize": pageSize,  # 每页数据数
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


