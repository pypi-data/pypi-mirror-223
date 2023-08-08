from setuptools import setup, find_packages

setup(
    name="proto-file",  # 包名，需要与 import 时的名称匹配
    version="0.2",  # 包的版本号
    packages=find_packages(),  # 自动找到所有的包
    python_requires=">=3.6",
)
