import allure

from service.app_a.asserts.order.asserts_order_mainorder import AssertsOrderMainorder
from service.app_a.apis.order import apis_order_mainorder
from service.app_a.funs.order.mainorder.funs_order_mainorder_scrm2app import FunsOrderMainorderScrm2App


class FunsOrderMainorder(AssertsOrderMainorder, FunsOrderMainorderScrm2App):
    @allure.step(title="小订订单分页查询（后台）-Y")
    def order_mainorder_pagelist(self, current=1, createEndTime="$None$", sortItems="$None$", createStartTime="$None$", size=10, _assert=True,  **kwargs):
        """
            url=/order/mainOrder/pageList
                params: current : string :
                params: size : string :
                params: sortItems : string : 排序字段（只能是【orderMain.orderType】、【orderMain.createTime】、【orderPay.createTime】）
                params: createStartTime : string : 订单创建开始日期
                params: createEndTime : string : 订单创建结束日期
                params: headers : 请求头
        """
        createEndTime = self.get_list_choice(createEndTime, list_or_dict=None, key="createEndTime")
        sortItems = self.get_list_choice(sortItems, list_or_dict=None, key="sortItems")
        createStartTime = self.get_list_choice(createStartTime, list_or_dict=None, key="createStartTime")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_mainorder.order_mainorder_pagelist(**_kwargs)

        self.assert_order_mainorder_pagelist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="小订订单列表导出（后台）-Y")
    def order_mainorder_download(self, createEndTime="$None$", orderTypeToSort="$None$", createStartTime="$None$", payTimeToSort="$None$", createTimeToSort="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/order/mainOrder/downLoad
                params: orderTypeToSort : string : 订单类型排序 不排序不赋值 正序：asc 倒序：desc
                params: createTimeToSort : string : 订单创建时间 不排序不赋值 正序：asc 倒序：desc
                params: payTimeToSort : string : 订单创建时间 不排序不赋值 正序：asc 倒序：desc
                params: createStartTime : string : 订单创建开始日期
                params: createEndTime : string : 订单创建结束日期
                params: headers : 请求头
        """
        createEndTime = self.get_value_choice(createEndTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        orderTypeToSort = self.get_value_choice(orderTypeToSort, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        createStartTime = self.get_value_choice(createStartTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        payTimeToSort = self.get_value_choice(payTimeToSort, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        createTimeToSort = self.get_value_choice(createTimeToSort, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_mainorder.order_mainorder_download(**_kwargs)

        self.assert_order_mainorder_download(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="小订订单查询订单详情（后台）-Y")
    def order_mainorder_detail(self, orderId="$None$", _assert=True,  **kwargs):
        """
            url=/order/mainOrder/detail
                params: orderId :  : 订单号
                params: headers : 请求头
        """
        orderId = self.get_list_choice(orderId, list_or_dict=None, key="orderId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_mainorder.order_mainorder_detail(**_kwargs)

        self.assert_order_mainorder_detail(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="订单管理-查询所有用户订单状态-Y")
    def order_mainorder_getuserorderstatuslist(self, _assert=True,  **kwargs):
        """
            url=/order/mainOrder/getUserOrderStatusList
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_mainorder.order_mainorder_getuserorderstatuslist(**_kwargs)

        self.assert_order_mainorder_getuserorderstatuslist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="订单管理-后台查询所有订单类型-Y")
    def order_mainorder_getordertypelist(self, _assert=True,  **kwargs):
        """
            url=/order/mainOrder/getOrderTypeList
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_mainorder.order_mainorder_getordertypelist(**_kwargs)

        self.assert_order_mainorder_getordertypelist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="订单管理-后台查询所有销售单订单状态-Y")
    def order_mainorder_getextorderstatuslist(self, _assert=True,  **kwargs):
        """
            url=/order/mainOrder/getExtOrderStatusList
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_mainorder.order_mainorder_getextorderstatuslist(**_kwargs)

        self.assert_order_mainorder_getextorderstatuslist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="订单管理-查询所有订单状态-Y")
    def order_mainorder_getorderstatuslist(self, _assert=True,  **kwargs):
        """
            url=/order/mainOrder/getOrderStatusList
                params: headers : 请求头
        """
        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_mainorder.order_mainorder_getorderstatuslist(**_kwargs)

        self.assert_order_mainorder_getorderstatuslist(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="订单管理-通过vin码查询订单-Y")
    def order_mainorder_vincode(self, vin="$None$", _assert=True,  **kwargs):
        """
            url=/order/mainOrder/vinCode
                params: vin :  : 车辆唯一vin码
                params: headers : 请求头
        """
        vin = self.get_list_choice(vin, list_or_dict=None, key="vin")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_mainorder.order_mainorder_vincode(**_kwargs)

        self.assert_order_mainorder_vincode(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="订单管理-订单完成-Y")
    def order_mainorder_finish(self, orderId="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/order/mainOrder/finish
                params: orderId : string :
                params: headers : 请求头
        """
        orderId = self.get_value_choice(orderId, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_mainorder.order_mainorder_finish(**_kwargs)

        self.assert_order_mainorder_finish(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="订单管理-查询订单权益接口-Y")
    def order_mainorder_allpricecontent(self, orderId="$None$", _assert=True,  **kwargs):
        """
            url=/order/mainOrder/allPriceContent
                params: orderId :  : 子订单号
                params: headers : 请求头
        """
        orderId = self.get_list_choice(orderId, list_or_dict=None, key="orderId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_mainorder.order_mainorder_allpricecontent(**_kwargs)

        self.assert_order_mainorder_allpricecontent(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="订单管理-通过用户ID查询订单ID-Y")
    def order_mainorder_getorderidbyuser(self, userId="$None$", _assert=True,  **kwargs):
        """
            url=/order/mainOrder/getOrderIdByUser
                params: headers : 请求头
        """
        userId = self.get_list_choice(userId, list_or_dict=None, key="userId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_mainorder.order_mainorder_getorderidbyuser(**_kwargs)

        self.assert_order_mainorder_getorderidbyuser(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="订单管理-通过订单号获取车型名称-Y")
    def order_mainorder__getmodelnamebyorderid(self, orderId="$None$", _assert=True,  **kwargs):
        """
            url=/order/mainOrder/=getModelNameByOrderId
                params: orderId :  :
                params: headers : 请求头
        """
        orderId = self.get_list_choice(orderId, list_or_dict=None, key="orderId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_mainorder.order_mainorder__getmodelnamebyorderid(**_kwargs)

        self.assert_order_mainorder__getmodelnamebyorderid(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="订单管理-通过订单号获取配置信息-Y")
    def order_mainorder_getcarconfigbyorderid(self, orderId="$None$", _assert=True,  **kwargs):
        """
            url=/order/mainOrder/getCarConfigByOrderId
                params: orderId :  :
                params: headers : 请求头
        """
        orderId = self.get_list_choice(orderId, list_or_dict=None, key="orderId")

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_mainorder.order_mainorder_getcarconfigbyorderid(**_kwargs)

        self.assert_order_mainorder_getcarconfigbyorderid(_assert, **_kwargs)
        self.set_output_value(_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="SCRM第三方订单同步信息-Y")
    def order_mainorder_syncscrmextorder(self, modelCode="$None$", customerCtCode="$None$", ossId="$None$", dealerCode="$None$", scUid="$None$", unitTaxNo="$None$", chargePointEquity="$None$", customerType="$None$", seriesCode="$None$", lifetimeWarrantyPrice="$None$", createTime="$None$", syncMsg="$None$", unitInvoiceTitle="$None$", trimCode="$None$", phone="$None$", colorCode="$None$", soNo="$None$", syncStatus="$None$", isArrived="$None$", orderNo="$None$", isTestDrive="$None$", custCertNo="$None$", configCode="$None$", VIN="$None$", potentialName="$None$", optionCode="$None$", soStatus="$None$", orderAllAmount="$None$", customerId="$None$", unitName="$None$", scUname="$None$", isLifetimeWarranty="$None$", orderId="$None$", updateTime="$None$", deliveryData="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/order/mainOrder/syncScrmExtOrder
                params: ossId : string : 主键
                params: dealerCode : string : 经销商代码
                params: customerId : number : 潜客 ID
                params: isArrived : string : 是否到店（true or false）
                params: isTestDrive : string : 是否试乘试驾（true or false）
                params: orderNo : string : 预订单单号
                params: orderId : number : 预订单订单 ID
                params: soNo : string : DMS 订单编号
                params: soStatus : string : 订单状态
                params: scUid : string : 销售顾问 ID
                params: scUname : string : 销售顾问姓名
                params: VIN : string : 车架号
                params: deliveryData : string : 承诺交车日期
                params: seriesCode : string : 车系代码
                params: modelCode : string : 车型代码
                params: configCode : string : 配置代码
                params: colorCode : string : 外观代码
                params: trimCode : string : 内饰代码
                params: optionCode : string : 选装包
                params: orderAllAmount : number : 订单价格(保留 3 位小数)
                params: customerType : string : 同步个人和企业
                params: potentialName : string : DMS 订单客户手机号
                params: phone : integer : DMS 订单客户证件类型
                params: customerCtCode : string : 证件号码
                params: custCertNo : string : 企业发票抬头
                params: unitName : string : 企业名称
                params: unitInvoiceTitle : string : 企业发票抬头
                params: unitTaxNo : integer : 企业税号
                params: chargePointEquity : integer : 充电桩权益      * 30471001: 7KW 充电桩      * 30471002: 11KW 充电桩      * 30471003: 家充桩置换公充权益      * 30471004:无电车权益
                params: isLifetimeWarranty : integer : (10041001 是, 10041002 否)
                params: lifetimeWarrantyPrice : string : 终身质保价格(保留 2 位小数)
                params: createTime : string : 创建订单时间
                params: updateTime : string : 更新订单时间
                params: syncStatus : integer : 0待同步，1同步成功，2同步失败
                params: syncMsg : string : 同步结果
                params: headers : 请求头
        """
        modelCode = self.get_value_choice(modelCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        customerCtCode = self.get_value_choice(customerCtCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        ossId = self.get_value_choice(ossId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        dealerCode = self.get_value_choice(dealerCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        scUid = self.get_value_choice(scUid, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        unitTaxNo = self.get_value_choice(unitTaxNo, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        chargePointEquity = self.get_value_choice(chargePointEquity, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        customerType = self.get_value_choice(customerType, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        seriesCode = self.get_value_choice(seriesCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        lifetimeWarrantyPrice = self.get_value_choice(lifetimeWarrantyPrice, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        createTime = self.get_value_choice(createTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        syncMsg = self.get_value_choice(syncMsg, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        unitInvoiceTitle = self.get_value_choice(unitInvoiceTitle, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        trimCode = self.get_value_choice(trimCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        phone = self.get_value_choice(phone, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        colorCode = self.get_value_choice(colorCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        soNo = self.get_value_choice(soNo, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        syncStatus = self.get_value_choice(syncStatus, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        isArrived = self.get_value_choice(isArrived, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        orderNo = self.get_value_choice(orderNo, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        isTestDrive = self.get_value_choice(isTestDrive, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        custCertNo = self.get_value_choice(custCertNo, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        configCode = self.get_value_choice(configCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        VIN = self.get_value_choice(VIN, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        potentialName = self.get_value_choice(potentialName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        optionCode = self.get_value_choice(optionCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        soStatus = self.get_value_choice(soStatus, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        orderAllAmount = self.get_value_choice(orderAllAmount, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        customerId = self.get_value_choice(customerId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        unitName = self.get_value_choice(unitName, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        scUname = self.get_value_choice(scUname, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        isLifetimeWarranty = self.get_value_choice(isLifetimeWarranty, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        orderId = self.get_value_choice(orderId, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        updateTime = self.get_value_choice(updateTime, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        deliveryData = self.get_value_choice(deliveryData, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_mainorder.order_mainorder_syncscrmextorder(**_kwargs)

        self.assert_order_mainorder_syncscrmextorder(_assert, **_kwargs)
        self.set_value(_kwargs)


    @allure.step(title="SCRM第三方转派经销商通知APP同步日志-Y")
    def order_mainorder_informorder(self, sourceInfo="$None$", systemCode="$None$", _assert=True, _all_is_None=False,  **kwargs):
        """
            url=/order/mainOrder/informOrder
                params: sourceInfo : array : 批量操作
                orderId : string : 订单ID
                customerId : number : 潜客ID
                dealerCode : string : 经销商代码(变更后的经销商)
                orderNo : number : 预订单单号
                soNo : string : DMS订单编号
                soStatus : string : 订单状态
                scUid : string : 销售顾问ID
                scUname : string : 销售顾问姓名
                params: systemCode : string : 变更系统
                params: headers : 请求头
        """
        sourceInfo = self.get_value_choice(sourceInfo, list_or_dict=None, key=None, _all_is_None=_all_is_None)
        systemCode = self.get_value_choice(systemCode, list_or_dict=None, key=None, _all_is_None=_all_is_None)

        _kwargs = self.get_kwargs(locals())
        self.res = apis_order_mainorder.order_mainorder_informorder(**_kwargs)

        self.assert_order_mainorder_informorder(_assert, **_kwargs)
        self.set_value(_kwargs)


