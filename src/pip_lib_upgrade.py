from pip._internal.utils.misc import get_installed_distributions as get_pip_list
from subprocess import  call

for dist in get_pip_list():
    print("check for " + dist.project_name)
    call("pip install --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple/ %s"%dist.project_name, shell=True)