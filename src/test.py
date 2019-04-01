from pyx import hello
import time
counter = 1
while True:
    hello.say_hello(str(counter))
    counter+=1
    time.sleep(1)
    if counter>5 :
        print('按回车键退出...')
        break
input('')