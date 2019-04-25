import os
mod_name = input('请输入需要安装的模块名称:')
if mod_name :
    with os.popen('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ %s' % mod_name) as f1:
        print(f1.read())
    with os.popen('pip list') as f2:
        print(f2.read())
    input('\r\nEnd.')