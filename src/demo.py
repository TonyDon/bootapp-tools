import time, os, sys
print(os.path.dirname(os.path.realpath((__file__))))
print(os.path.dirname(os.path.realpath(sys.executable)))
print(getattr(sys, 'frozen', False))
print(sys.argv[1])
tmpdir_list = os.listdir(r'c:\tmpdir')
for dir_path in tmpdir_list:
    abs_dir_path = r'c:\tmpdir\%s' % (dir_path)
    dir_st = os.stat(abs_dir_path)
    print(abs_dir_path, dir_st.st_mtime)
