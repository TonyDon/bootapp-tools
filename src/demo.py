import time, os, sys
print(os.path.dirname(os.path.realpath((__file__))))
print(os.path.dirname(os.path.realpath(sys.executable)))
print(getattr(sys, 'frozen', False))
time.sleep(5)