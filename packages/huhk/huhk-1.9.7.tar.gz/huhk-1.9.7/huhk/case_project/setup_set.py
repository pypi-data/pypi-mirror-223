from setuptools import setup, find_packages

from unit_fun import FunBase


def find_data_files(directory):
    pass


setup(
    name='huhk',  # 对外模块的名字
    version=FunBase.get_version(),  # 版本号
    description='接口自动化',  # 描述
    author='胡杭凯',  # 作者
    author_email='3173825608@qq.com',
    package_dir={"huhk": "huhk", "huhk.allure.bin": "huhk/allure/bin"},
    packages=find_packages(where=".", exclude=(), include=("*",)),
    # data_files={"documentation": find_data_files()},
    include_package_data=True,
    # data_files=[("bin", ["huhk/allure/bin"])],
    # ext_modules=["huhk/allure"],
    entry_points={'console_scripts': ['huhk=huhk.main:main']},
    python_requires=">=3.0",
    install_requires=[
        "faker",
        "openpyxl",
        "apscheduler",
        "rsa",
        "pyDes",
        "pycryptodome",
        "xlsxwriter",
        "pandas",
        "apache-beam",
        "pytest",
        "setuptools",
        "twine",
        "requests==2.29.0",
        "pandas",
        "click",
    ],
)


