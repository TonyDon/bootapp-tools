import time
import random

async def calc(code_no):
    time.sleep(random.randint(1,3))
    return 'calc-{}-done. at {}'.format(code_no, time.strftime("%Y-%m-%d %H:%M:%S"))

async def handler():
    box = ['1','2','3','4','5']
    for s in box:
            print('begin calc.', s)
            result = await calc(s)
            print('end calc.', s, result)
    
def run_coroutine(co):
    try:
        co.send(None)
    except StopIteration as e :
        print(str(e))
    
if __name__ == '__main__':
    run_coroutine(handler())
    time.sleep(5)