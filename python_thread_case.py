 1 # -*- coding: utf-8 -*- 
 2 import unittest,time,sys 
 3 sys.path.append("..") 
 4 from public import HTMLTestRunner 
 5 class test(unittest.TestCase): 
 6     def setUp(self): 
 7         pass 
 8     def test_login(self): 
 9         u"""test_1 test1 登录用例login""" 
10         time.sleep(5) 
11         pass 
12     def test_process(self): 
13         u"""test_1 test1 处理用例login""" 
14         time.sleep(5) 
15         assertEqual(1,2) 
16     def test_quit(self): 
17         u"""test_1 test1 登录用例quit""" 
18         time.sleep(5) 
19         self.assertEqual(1,2) 
20     def tearDown(self): 
21         pass 
22 if  __name__==‘__main__‘: 
23     suit=unittest.TestSuite() 
24     filename=sys.argv[1] 
25     suit.addTest(unittest.makeSuite(test)) 
26     f=open(filename,"wb") 
27     runner = HTMLTestRunner.HTMLTestRunner( 
28              stream=f, 
29              title=u‘测试报告‘, 
30              description=u‘测试结果‘) 
31     runner.run(suit) 