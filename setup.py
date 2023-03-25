from setuptools import setup, find_packages

setup(
    name='hiyobot', # 你的项目名称
    version='0.0.8', # 你的项目版本
    description='A simple bot framework for Hack.chat.', # 你的项目简介
    long_description=open('README.md').read(), # 你的项目详细介绍，一般从README.md文件中读取
    long_description_content_type='text/markdown', # 你的项目详细介绍的格式，一般为markdown格式
    url='https://github.com/Hiyoteam/hiyobot', # 你的项目主页，一般为github仓库地址
    author='MaggieLOL', # 你的姓名或者团队名称
    author_email='tanhanzesnd@gmail.com', # 你的邮箱或者团队邮箱
    license='GPL-2.0', # 你的项目使用的许可证，一般为MIT或者其他开源许可证
    classifiers=[ # 你的项目分类信息，可以从https://pypi.org/classifiers/中选择合适的分类
        'Development Status :: 3 - Alpha', # 开发状态，一般为Alpha（初级）、Beta（中级）或者Stable（稳定）
        'Intended Audience :: Developers', # 目标受众，一般为Developers（开发者）、End Users/Desktop（桌面端用户）等
        'Topic :: Software Development :: Libraries :: Python Modules', # 主题，一般为Software Development（软件开发）、Scientific/Engineering（科学/工程）等
        'Programming Language :: Python :: 3', # 编程语言，一般为Python :: 3或者Python :: 2
        'Programming Language :: Python :: 3.10', # 编程语言的具体版本，根据你的项目支持的python版本选择
    ],
    keywords='bot hack.chat hack.chat-bot', # 一些关键词，用于描述你的项目特点或者功能
    packages=find_packages(), # 需要打包的python模块，一般使用find_packages函数自动查找，排除测试模块等不需要打包的模块
    install_requires=[ # 需要安装的依赖包，一般从requirements.txt文件中读取或者手动列出
        'websocket-client',
        'uuid',
    ],
)
