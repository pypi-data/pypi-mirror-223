import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke:冒烟用例")
    config.addinivalue_line("markers", "success:正向用例")
    config.addinivalue_line("markers", "failed:逆向用例")
    config.addinivalue_line("markers", "get:查询用例")
    config.addinivalue_line("markers", "fun:功能用例")

