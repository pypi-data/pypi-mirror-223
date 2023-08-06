from setuptools import setup

"""
必填参数：
    名称：name = "xxxx"
    版本：version = "1.0.0"
    描述信息：description= "xxxxxxxxxxx"
    需要处理的包列表(可能有多个包) packages = ["zcytestlib","zcytestlib2"]
可选参数
    作者： author = "ZCY"
    需要处理的但文件模块列表 py_modules = ["",""] 
    作者邮箱：author_email = "zcyang098@163.com"
    长描述：long_description = "这里的字符串可以从README.rst文件中读取进来",展示在pypi首页里与README.rst与定
    
"""


# 命令 python setup.py check -r -s  来检查long_description的中语法是否有问题，传到pypi是否会出现未渲染的情况

def readme_file():
    with open("README.rst", encoding="utf-8") as rf:
        return rf.read()


setup(name="zcytestlib",
      version="1.0.1",
      description="this is a zcy demo lib ",
      packages=["zcytestlib"],
      py_modules=["tool"],
      author="ZCY",
      author_email="zcyang098@163.com",
      long_description=readme_file(),
      url="https://github.com/aheake/zcyTest", license="MIT")

# 回到当前项目地址，终端输入python setup.py sdist ，生成一个dist文件夹，里边即为当前项目的压缩包
"""
LICENSE.txt 声明库的使用责任，所有权归属，别人是否可以对代码进行任何操作，是否可用于其它商业用途等
            文件内容获取地址：https://choosealicense.com/
MANIFEST.in 该文件可以控制打包应该包含哪些文件（通过编写配置文件） 如 include c  （打包时候自动识别c文件，并将其加入目标包）
            
            --如requests包的MANIFEST.in文件内容--
            include README.md LICENSE NOTICE HISTORY.md pytest.ini requirements-dev.txt
            recursive-include tests *.py
"""

"""
------------------打包-----------------------------------------------------------------------------------
1.  python setup.py sdist 
    生成源码压缩包，包含setup.py 模块源文件，数据文件等等，可以在任何平台上重新编译所有内容
    --formats = 压缩格式1，压缩格式2
2.  python setup.py sdist --formats==zip,tar
    指明压缩格式

3.  python setup.py bdist:  
    生成二进制发行包（已经编译好了， .pyc代表编译后的文件），不包括setup.py ，是某个特定平台和Python的一个存档，并且包括源码

4.  python setup.py bdist_egg:
    生成egg格式的二进制包(需要安装setuptools包)
5.  python setup.py bdist_wheel:
    生成wheel格式的二进制包(需要安装wheel)
6.  python setup.py bdist_wininst:
    生成windows下的安装包()
------------------安装------------------------------------------------------------------------------------
    带setup.py的
    1.解压    进入setup.py同级目录，执行python setup.py install
    2.        easy_install xxxx.zip 
    3.        pip install xxx.zip
    
    二进制发行包：
    1.         将xxxxamd64.zip 解压后打开最里层文件夹，copy到当前环境site_packages下
    2.          easy_install xxxx.egg
                pip install xxxx.whl
------------------上传至pypi--------------------------------------------------------------------------------
       twine upload xxxx.zip 
       输入对应的账号和密码即可        
"""
