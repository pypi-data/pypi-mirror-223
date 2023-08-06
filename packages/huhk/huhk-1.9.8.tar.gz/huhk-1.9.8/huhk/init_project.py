import os.path
import re

from huhk.case_project.project_base import ProjectBase
from huhk.unit_dict import Dict
from huhk.unit_fun import FunBase
from huhk import projects_path


class GetApi(ProjectBase):
    def __init__(self, name=None, app_key=None, yapi_url=None, yapi_token=None, yapi_json_file=None, swagger_url=None):
        """
        """
        super().__init__(name, app_key, yapi_url, yapi_token, yapi_json_file, swagger_url)
        self.get_project()

    def create_or_update_project(self, _update=False):
        """
        创建项目
        """
        # 创建项目目录
        self.set_file_path()
        # 获取已维护api方法接口列表
        self.get_this_fun_list()
        # 获取接口文档api接口列表
        self.get_api_list()
        # 添加api封装方法
        self.write_fun(_update=_update)

    def set_file_path(self):
        """创建项目框架"""
        FunBase.mkdir_file(self.path.values(), is_py=True)
        if not os.path.exists(os.path.join(self.path.service_dir, "__init__.py")) or \
                not FunBase.read_file(os.path.join(self.path.service_dir, "__init__.py")):
            FunBase.write_file(os.path.join(self.path.service_dir, "__init__.py"), value=self.get_init_value())
        if not os.path.exists(os.path.join(self.path.service_dir, f"{self.name}_fun.py")):
            FunBase.write_file(os.path.join(self.path.service_dir, f"{self.name}_fun.py"), value=self.get_fun_value())
        if not os.path.exists(os.path.join(self.path.service_dir, f"setting.json")):
            FunBase.write_file(os.path.join(self.path.service_dir, f"setting.json"), value="{}")
        if not os.path.exists(os.path.join(self.path.testcase_dir, f"conftest.py")):
            FunBase.write_file(os.path.join(self.path.testcase_dir, f"conftest.py"), value=self.get_conftest_value())

    def get_api_fun_list(self):
        """获取已维护方法列表，无则创建demo文件"""
        self.path.fun_file_path = os.path.join(self.path.service_dir, self.name + "_fun.py")
        if os.path.exists(self.path.fun_file_path):
            self.fun_file_str = FunBase.read_file(self.path.fun_file_path)
        else:
            self.fun_file_str = "import requests\n\nfrom huhk.unit_fun import FunBase\n" \
                                "from huhk import admin_host\n\n\nclass %sFun(FunBase):\n" \
                                "    def __init__(self):\n        super().__init__()\n        self.res = None\n\n" \
                                "    def run_mysql(self, sql_str):\n" \
                                "        # id是后台http://47.96.124.102/admin 项目数据库链接的id\n" \
                                '        out = requests.post(admin_host + "/sql/running_sql/", ' \
                                'json={"id": 1, "sql_str": sql_str}).json()\n' \
                                '        if out.get("code") == "0000":\n' \
                                '            return out.get("data")\n        else:\n' \
                                '            assert False, sql_str + str(out.get("msg"))\n\n\n' \
                                "if __name__ == '__main__':\n    f = %sFun()\n" \
                                '    out = f.run_mysql("SELECT * FROM `t_accept_log`  LIMIT 1;")\n' \
                                '    print(out)\n\n' % (self.name2, self.name2)
        self.fun_init_str = re.findall(r"(def +[\d\D]*?\n)\s*def", self.fun_file_str)[0]
        self.fun_init_list = [i.split('=')[0].strip()[5:] for i in self.fun_init_str.split('\n') if "=" in i]

        self.path.sql_file_path = os.path.join(self.path.service_dir, self.name + "_sql.py")
        if os.path.exists(self.path.sql_file_path):
            self.sql_file_str = FunBase.read_file(self.path.sql_file_path)
        else:
            self.sql_file_str = "from service.%s.%s_fun import %sFun\n\n\n" % (self.name, self.name, self.name2)
            self.sql_file_str += "class %sSql(%sFun):\n\n\n" \
                                 "if __name__ == '__main__':\n    s = %sSql()\n\n" % (
                                     self.name2, self.name2, self.name2)
        self.sql_fun_list = re.findall("    def +(.*)?\(", self.sql_file_str)

        self.path.assert_file_path = os.path.join(self.path.service_dir, self.name + "_assert.py")
        if os.path.exists(self.path.assert_file_path):
            self.assert_file_str = FunBase.read_file(self.path.assert_file_path)
        else:
            self.assert_file_str = "import allure\n\nfrom service.%s.%s_sql import %sSql\n\n\n" % (
            self.name, self.name, self.name2)
            self.assert_file_str += "class %sAssert(%sSql):\n\n\n" \
                                    "if __name__ == '__main__':\n    s = %sAssert()\n\n" % (
                                        self.name2, self.name2, self.name2)
        self.assert_fun_list = re.findall("    def +(.*)?\(", self.assert_file_str)

        self.path.api_fun_file_path = os.path.join(self.path.service_dir, self.name + "_api_fun.py")
        if os.path.exists(self.path.api_fun_file_path):
            self.api_fun_file_str = FunBase.read_file(self.path.api_fun_file_path)
        else:
            self.api_fun_file_str = "from service.%s.%s_assert import %sAssert\n" % (self.name, self.name, self.name2)
            self.api_fun_file_str += "from service.%s import %s_api\n\nimport allure\n" % (self.name, self.name)
            self.api_fun_file_str += "\n\nclass %sApiFun(%sAssert):\n\n" \
                                     "if __name__ == '__main__':\n    s = %sApiFun()\n\n" % (
                                         self.name2, self.name2, self.name2)
        self.api_fun_fun_list = re.findall("    def +(.*)?\(", self.api_fun_file_str)

        self.path.api_testcase_file_path = os.path.join(self.path.testcase_dir, "test_api.py")
        if os.path.exists(self.path.api_testcase_file_path):
            self.api_testcase_file_str = FunBase.read_file(self.path.api_testcase_file_path)
        else:
            self.api_testcase_file_str = "import pytest\nimport allure\n\n" \
                                         "from service.%s.%s_api_fun import %sApiFun\n\n\n" % (
                                             self.name, self.name, self.name2)
            self.api_testcase_file_str += '@allure.epic("针对单api的测试")\n@allure.feature("场景：")\nclass TestApi:\n' \
                                          '    def setup(self):\n        self.f = %sApiFun()\n\n' % self.name2
        self.api_testcase_list = re.findall("    def +test_(.*)?\(", self.api_testcase_file_str)

    def get_api_list(self):
        """根据api文档不同方式生成api文件"""
        if self.swagger_url:
            self.get_list_menu_swagger()
        elif self.yapi_url and self.yapi_token:
            self.get_list_menu()
        elif self.yapi_file_str or self.yapi_json_file:
            self.get_list_json()

    def write_fun(self, _update=False):
        if not self.this_fun_list.api and not self.api_list:
            self.api_list += [{'method': 'GET', 'title': '示例-get', 'path': '/demo/get', 'up_time': 1675665418},
                              {'method': 'POST', 'title': '示例-post', 'path': '/demo/post', 'up_time': 1675665418}]
        for row in self.api_list:
            self.write_api(row)
        for fun_name in self.this_fun_list.api.keys():
            self.write_sql(fun_name, _update=_update)
            self.write_assert(fun_name, _update=_update)
            self.write_api_fun(fun_name, _update=_update)
            self.write_testcase(fun_name, _update=_update)

    def sub_hz(self, _id, _str):
        if re.findall(r'[^\da-zA-Z_\ (=,*):]', re.findall(r"def .*?\):", _str)[0]):
            api = self.get_api(_id)
            tmp2 = api.get('data', {}).get('req_params', [])
            for tmp3 in tmp2:
                name = tmp3.get('name', "")
                desc = tmp3.get('desc', "")
                if re.findall(r'[^\da-zA-Z_\ (=,*):]', name) and not re.findall(r'\W', desc):
                    _str = _str.replace(name, desc)
        if re.findall(r'[( ]async[,=)]', _str):
            for tmp in re.findall(r'[( ]async[,=)]', _str):
                tmp1 = str(tmp).replace('async', 'async1')
                _str = _str.replace(tmp, tmp1)
        return _str

    @staticmethod
    def get_main_key():
        return GetApi._get_service_value("this_key", _type=1)

    @staticmethod
    def set_main_key(value):
        GetApi._set_service_value("this_key", value, _type=1)
        return True

    @staticmethod
    def get_main_name():
        return GetApi._get_service_value("this_name", _type=1)

    @staticmethod
    def set_main_name(value):
        GetApi._set_service_value("this_name", value, _type=1)

    @staticmethod
    def get_key_name_list(path=None):
        out = Dict()
        path = path or projects_path
        for dirpath, dirnames, filenames in os.walk(path):
            if "apis" in dirnames and "asserts" in dirnames and "funs" in dirnames and "sqls" in dirnames \
                    and "__init__.py" in filenames:
                name = os.path.basename(dirpath)
                init_str = FunBase.read_file(os.path.join(dirpath, "__init__.py"))
                app_key = re.findall(r'\nAPP_KEY *= *[\'\"](.+)[\'\"]', init_str)
                app_key = app_key[0] if app_key else None
                if app_key:
                    out[name] = app_key
                    out[app_key] = name
                else:
                    out[name] = None
        if out:
            return out
        else:
            if os.path.exists(os.path.dirname(path)) and len(path) > 5:
                return GetApi.get_key_name_list(os.path.dirname(path))
        return out


if __name__ == '__main__':
    ga = GetApi()
    print(ga.get_key_name_list())