import requests

from huhk.unit_fun import FunBase
from huhk.unit_dict import Dict
from huhk import admin_host


class AppAFun(FunBase):
    def __init__(self):
        super().__init__()
        self.res = None
        self.output_list = Dict()
        self.input_value = Dict()
    @staticmethod
    def run_mysql( sql_str, db_id=1):
        # 根据后台数据库配置id查询
        out = requests.post(admin_host + "/sql/running_sql/", json={"id": db_id, "sql_str": sql_str}).json()
        if out.get("code") == "0000":
            return out.get("data")
        else:
            assert False, sql_str + str(out.get("msg"))


if __name__ == '__main__':
    f = AppAFun()
    out = f.faker().name()
    print(out)

