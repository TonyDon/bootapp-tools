import os,subprocess
from subprocess import Popen,call
mod_name = input('请输入需要安装的模块名称:')
if mod_name :
    with Popen('pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ %s' % mod_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as f1:
        while True:
            buff = f1.stdout.readline()
            ret = Popen.poll(f1)
            line = None
            if buff :
                line = buff.decode(encoding='utf-8').strip('\r\n')
                print('...',line)
            if  ret is not None:
                print('\r\n...exec finish.')
                break
            
    call('pip list', shell=True)
    input('\r\n...End.')