#!/usr/bin/env python
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'requirements.txt'), 'r', encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

with open(path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]

setup(
    name='aisrfwk',  # 必填，项目的名字，用户根据这个名字安装，pip install SpiderKeeper-new
    version='1.0.5',  # 必填，项目的版本，建议遵循语义化版本规范
    author='wmang',  # 项目的作者
    description='aisr ai framework,稳定版,修复最终推送状态错误bug',  # 项目的一个简短描述
    long_description=long_description,  # 项目的详细说明，通常读取 README.md 文件的内容
    long_description_content_type='text/markdown',  # 描述的格式，可选的值： text/plain, text/x-rst, and text/markdown
    author_email='wangmian05@countrygarden.com.cn',  # 作者的有效邮箱地址
    url='https://blog.csdn.net/a249040113?type=blog',  # 项目的源码地址
    license='MIT',
    include_package_data=True,
    packages=find_packages(),  # 必填，指定打包的目录，默认是当前目录，如果是其他目录比如 src, 可以使用 find_packages(where='src')
    install_requires=install_requires,  # 指定你的项目依赖的 python 包，这里直接读取 requirements.txt
    # 下面的设置将在命令行提供一个叫做 spiderkeeper 的命令，用来执行 SpiderKeeper 包下 run 的 main 方法启动项目
    # entry_points={
    #     'console_scripts': {
    #         'aisrfwk = aisrfwk.run:main'
    #     },
    # },
    # 分类器通过对项目进行分类，帮助用户找到项目
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',

)
