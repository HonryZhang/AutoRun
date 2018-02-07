import thread
import threading
import Queue
import time
from time import ctime,sleep

def read(q, number):
    while True:
        try:
            value = q.get()
            print('Get %s from queue.time is' % value )
            print number
            sleep(5)
            #time.sleep(random.random())
        finally:
            q.task_done()

def main():
    q = Queue.Queue()
    pw1 = threading.Thread(target=read, args=(q,1))
    pw2 = threading.Thread(target=read, args=(q,2))
    pw1.daemon = True
    pw2.daemon = True
    pw1.start()
    pw2.start()
    for c in [chr(ord('A')+i) for i in range(26)]:
        q.put(c)
    try:
        q.join()
    except KeyboardInterrupt:
        print("stopped by hand")

if __name__ == '__main__':
    main()