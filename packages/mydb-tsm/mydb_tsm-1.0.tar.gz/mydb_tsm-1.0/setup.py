from distutils.core import setup

with open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

setup(
    name='mydb_tsm',  # 对外我们模块的名字
    version='1.0',  # 版本号
    long_description=long_description,  # 包的描述
    long_description_content_type='text/markdown',  # 包描述的类型
    author='Tomboy',  # 作者
    author_email='Tomboy1996@163.com',  # 作者邮箱
    py_modules=['mydb_tsm.mydb_tsm', 'mydb_tsm.test'],  # 要发布的模块
)