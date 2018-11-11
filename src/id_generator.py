import time
import threading
    
#
# id sequence generator
# 序列号生成器 ，毫秒时间差值+worker编号（4bit)+自增值(12bit)
#
class IdGenerator(object):
    
    workerNo = None
    spanTime = 1535731200000
    incrSeq = 0
    lastTime = None
    
    def __init__(self, workerNo=0):
        self.workerNo = (workerNo<<12)
        self.lastTime = self.__getTime()
        pass
    
    def get(self):
        curTime = self.__getTime()
        if curTime==self.lastTime :
            if self.incrSeq<4095:
                self.incrSeq+=1
                diffTime = (curTime - self.spanTime) <<16
                seq_id = diffTime | self.workerNo | self.incrSeq
            else:
                self.incrSeq=0
                time.sleep(0.001)
                curTime = self.__getTime()
                if curTime>self.lastTime :
                    self.lastTime = curTime
                    diffTime = (curTime - self.spanTime) <<16
                    seq_id = diffTime | self.workerNo | self.incrSeq
                else:
                    raise Exception("time error")
        else:
            self.incrSeq=0
            self.lastTime = curTime
            diffTime = (curTime - self.spanTime) <<16
            seq_id = diffTime | self.workerNo | self.incrSeq
        return seq_id
        pass
    
    def __getTime(self):
        return int(time.time() * 1000)
    
    

class Consumer(threading.Thread):
    idGenerator = None
    box = None
    def __init__(self, idGenerator=None, box=None, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self.idGenerator = idGenerator

        
    def run(self):
        threading.Thread.run(self)
        if self.idGenerator :
            idv = self.idGenerator.get()
            box.add(idv)
            print(idv)
        
        
if __name__ == '__main__' :
    idGen = IdGenerator(workerNo=1)
    box =set()
    for i in range(5000):
        client = Consumer(idGenerator=idGen)
        client.start()
    time.sleep(10)
    print(len(box))
    print(box.pop())
    print(box.pop())
    print(box.pop())
    print(box.pop())
    print(box.pop())
    print(box.pop())
    print(box.pop())
        