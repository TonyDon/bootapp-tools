import os
import subprocess
import time

th_mvn_dir=r'C:\maven_tuhu_rep\com\tuhu'

def force_remove_file(curr_file_path:str):
    if os.path.isdir(curr_file_path) :
        child_files = os.listdir(curr_file_path)
        for f in child_files:
            child_file_path = os.path.join(curr_file_path, f)
            force_remove_file(child_file_path)
        os.rmdir(curr_file_path)
        print( '--remove dir : %s' % curr_file_path)
    elif os.path.isfile(curr_file_path) :
        os.remove(curr_file_path)
        print( '--remove file : %s' % curr_file_path)
    pass

files  = os.listdir(th_mvn_dir)
for f in files:
    if 'hp' in f or 'huapei' in f :
        curr_file_path = os.path.join(th_mvn_dir, f)
        print(curr_file_path)
        force_remove_file(curr_file_path)
     
time.sleep(1)
	 
subprocess.call('cmd /C explorer.exe {0}'.format(th_mvn_dir), shell=True)
