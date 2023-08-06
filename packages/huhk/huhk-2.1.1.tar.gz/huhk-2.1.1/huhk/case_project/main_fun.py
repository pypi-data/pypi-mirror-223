import click

from huhk.case_project.version import version as _version
from huhk.init_project import GetApi


def get_version():
    k = str(GetApi.get_main_key())
    v = str(GetApi.get_main_name())
    out_str = f"版本：{_version}\n--key：{k}\n--name：{v}"
    return out_str


def set_key_name(key, name):
    if key and name:
        GetApi.set_main_key(key)
        GetApi.set_main_name(name)
    elif key or name:
        key_list = GetApi.get_key_name_list()
        if key:
            GetApi.set_main_key(key)
            if key_list.get(key):
                GetApi.set_main_name(key_list.get(key))
        else:
            if key_list.get(name):
                GetApi.set_main_key(key_list.get(name))
            GetApi.set_main_name(name)
    return True


def install_project(app_key, name=None):
    ga = GetApi(name=name, app_key=app_key)
    ga.create_or_update_project()
    set_key_name(app_key, name)
    return "项目创建成功"


def update_project(app_key=None, name=None):
    set_key_name(app_key, name)
    app_key = GetApi.get_main_key()
    name = GetApi.get_main_name()
    if not app_key and not name:
        return "项目未指定，请指定参数-k/-n"
    else:
        ga = GetApi(name=name, app_key=app_key)
        ga.create_or_update_project()
        return "项目更新成功"


def fun_project(app_key=None, name=None, fun_url=None, method=None):
    set_key_name(app_key, name)
    app_key = GetApi.get_main_key()
    name = GetApi.get_main_name()
    if not app_key and not name:
        return "项目未指定，请指定参数-k/-n"
    else:
        ga = GetApi(name=name, app_key=app_key)
        methods = {1: "GET", 2: "POST", 3: "PUT", 4: "DELETE",
                   5: "HEAD", 6: "OPTIONS", 7: "PATCH", 8: "CONNECT"}
        while not method:
            method = input("输入方法类型（回车默认：get）：")
            if method == "":
                method = "GET"
            elif method.isdigit() and int(method) < 9:
                method = methods[int(method)]
            elif method.upper() in methods.values():
                method = method.upper()
            else:
                print(f"""输入类型错误，请重新输入：{methods}""")
                method = None
        if method == "POST":
            headers_list = {0: {"Content-Type": "application/json"},
                            1: {"Content-Type": "application/x-www-form-urlenc"},
                            2: {"Content-Type": "multipart/form-data"},
                            3: {"Content-Type": "text/xml"}}
            while not headers:
                headers = input("输入post请求类型（回车默认：application/json）：")
                if method == "":
                    headers = headers_list[0]
                elif method.isdigit() and int(method) < 4:
                    headers = headers_list[int(method)]
                else:
                    try:
                        headers = eval(headers)
                    except:
                        print(f"""输入类型错误，请重新输入\n""")
                        headers = None

        return "方法添加/更新成功"


def running_testcase(running):
    running_path_list = []
    for cases in running:
        for case in cases.split(","):
            running_path = GetApi.get_running_path(case)
            running_path_list.append(running_path)
    print(running_path_list)
    return "执行用例完成"
