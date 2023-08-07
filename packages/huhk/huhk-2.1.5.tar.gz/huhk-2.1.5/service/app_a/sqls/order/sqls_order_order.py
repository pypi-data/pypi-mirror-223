from service.app_a.app_a_fun import AppAFun


class SqlsOrderOrder(AppAFun):
    def sql_order_order_orderdetail(self, **kwargs):
        # name = self.kwargs_pop(kwargs, 'name')  # 单独处理字段
        # self.kwargs_replace(kwargs, likes=[], ins=[], before_end=[])  # 模糊查询字段，数组包含查询字段，区间字段处理
        # kwargs["order_by"] = None  # 排序
        sql_str = self.get_sql_str("table_name", **kwargs)  # 生成sql语句
        # out = self.run_mysql(sql_str)  # 执行sql语句
        # return out

    def sql_order_order_finish(self, **kwargs):
        # name = self.kwargs_pop(kwargs, 'name')  # 单独处理字段
        # self.kwargs_replace(kwargs, likes=[], ins=[], before_end=[])  # 模糊查询字段，数组包含查询字段，区间字段处理
        # kwargs["order_by"] = None  # 排序
        sql_str = self.get_sql_str("table_name", **kwargs)  # 生成sql语句
        # out = self.run_mysql(sql_str)  # 执行sql语句
        # return out

    def sql_order_order_refundreject(self, **kwargs):
        # name = self.kwargs_pop(kwargs, 'name')  # 单独处理字段
        # self.kwargs_replace(kwargs, likes=[], ins=[], before_end=[])  # 模糊查询字段，数组包含查询字段，区间字段处理
        # kwargs["order_by"] = None  # 排序
        sql_str = self.get_sql_str("table_name", **kwargs)  # 生成sql语句
        # out = self.run_mysql(sql_str)  # 执行sql语句
        # return out

