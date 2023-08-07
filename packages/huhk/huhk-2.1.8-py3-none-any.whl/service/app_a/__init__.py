from huhk.init_project import GetApi
from huhk.unit_request import UnitRequest


class Request(UnitRequest):
    pass


APP_KEY = "4ab5ebca-77d6-470e-9a3d-417f917ea85f"


unit_request = Request("SIT", APP_KEY)
# 环境变量
variable = unit_request.variable
http_requester = unit_request.http_requester


if __name__ == "__main__":
    GetApi(name='app_a', app_key=APP_KEY).create_or_update_project()
