import zcytestlib

"""
    由于在zcytestlib 这个packages里的__init__方法里定义了导入zcylibone这个子文件，
    因此在导入这个包时候，就会导入该子文件，访问时候以属性方式访问
"""
zcytestlib.zcylibone.run()


def tt():
    print("tool")
