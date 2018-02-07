 1 #! /usr/bin/env python 
 2 #coding=utf-8 
 3 import threading 
 4 from multiprocessing import Queue 
 5 from time import ctime,sleep 
 6 from subprocess import Popen,PIPE 
 7 import os,time 
 8 lock=threading.Lock() 
 9 #单个测试用例生成的临时报告,当前目录下result\temp_年月日_时分秒\文件目录.html 
10 #例如 E:\python\selenium\fortest\result\temp_20160704_102822\E_python_selenium_fortest_test_1_test1_py.html 
11 def resultfile(tempdir,file): 
12     name=file.replace(‘\\‘,‘_‘).replace(‘:‘,‘‘).replace(‘.‘,‘_‘)+‘.html‘ 
13     return os.path.join(tempdir,name) 
14 class MyThread(threading.Thread): 
15     def __init__(self,queue,tempresultdir): 
16         threading.Thread.__init__(self) 
17         self.queue=queue 
18         self.tempresultdir=tempresultdir 
19     def run(self): 
20         while True: 
21             if not self.queue.empty(): 
22                 filename=self.queue.get() 
23                 lock.acquire() 
24                 resultname=resultfile(self.tempresultdir,filename) 
25                 cmd="python "+filename+" "+resultname 
26                 #print cmd 
27                 print ‘start time:%s‘ %ctime() 
28                 lock.release() 
29                 p=Popen(cmd,shell=True,stdout=PIPE) 
30                 #如果不加如下print,不会等待执行完毕 
31                 print p.stdout.readlines() 
32             else: 
33                 print ‘end‘ 
34                 break 
35 #获取路径下test开头的文件夹下以test开头.py结尾的文件 
36 def getfile(path): 
37     paths=[] 
38     for p in os.listdir(path): 
39         if p[0:4]==‘test‘ and os.path.isdir(p): 
40             paths.append(p) 
41     file=[] 
42     for p in paths: 
43         temp=os.path.join(path,p) 
44         #print temp 
45         files=os.listdir(temp) 
46         #print files 
47         for f in files: 
48             if f[0:4]==‘test‘ and f[-3:]==‘.py‘: 
49                 file.append(os.path.join(temp,f)) 
50     return file 
51 if __name__==‘__main__‘: 
52     print ‘main start time:%s‘ %ctime() 
53     tempresultdir=os.path.join(os.getcwd(),"result","temp"+time.strftime("_%Y%m%d_%H%M%S",time.localtime(time.time()))) 
54     os.mkdir(tempresultdir) 
55     resultreport=os.path.join(os.getcwd(),"result"+time.strftime("_%Y%m%d_%H%M%S",time.localtime(time.time()))) 
56     allfile=getfile(os.getcwd()) 
57     queue=Queue() 
58     for file in allfile: 
59         queue.put(file) 
60     my_Threads=[] 
61     my_Thread=threading.Thread() 
62     for i in range(2): 
63         my_Thread=MyThread(queue,tempresultdir) 
64         my_Thread.deamon=True 
65         my_Threads.append(my_Thread) 
66         my_Thread.start() 
67     for t in my_Threads: 
68         t.join()
69 
70     reports=os.listdir(tempresultdir) 
71     print reports 
72     print ‘main end time:%s‘ %ctime()