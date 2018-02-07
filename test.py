from lib.ceph.lib.ceph.lib.ceph.lib import *
import logs

#logs.LogRecord('reliablitly', 'E:\\Becky_automation\\reliability-test\\reliabilitylog.txt')
#osdObj = osd('22','345')
#osdObj.shutdown('192.168.28.57')
#osdObj.kill('192.168.28.57')

import re
from wx.lib.agw.peakmeter import InRange
'''
def delblankline(infile, outfile):
    """ Delete blanklines of infile """
    infp = open(infile, "r")
    outfp = open(outfile, "w")
    lines = infp.readlines()
    for li in lines:
        #if li.strip():
            #outfp.writelines(li)
        newli = li.replace(" ","").replace("\t","").strip()
        outfp.writelines(newli)
    infp.close()
    outfp.close()
'''
infile = "C:\\Users\\admin\\workspace\\reliablity\\ceph.conf"

outfile = "C:\\Users\\admin\\workspace\\reliablity\\ceph_test.conf"

output = '''
    cluster 2ec052f8-599b-4cd9-86fc-4f8382d65d06
     health HEALTH_OK
     monmap e1: 1 mons at {425-1=192.168.28.57:6789/0}
            election epoch 3, quorum 0 425-1
     osdmap e110: 9 osds: 9 up, 9 in
            flags sortbitwise,require_jewel_osds,require_kraken_osds
      pgmap v228901: 3072 pgs, 12 pools, 2032 bytes data, 206 objects
            9238 MB used, 52114 MB / 61353 MB avail
                3072 active+clean
  client io 23714 B/s rd, 26 op/s rd, 0 op/s wr
'''

#status = re.compile(reg)
print output
for line in output:
    print line
print output.find("health")

#delblankline(infile,outfile)   
'''
f = open(infile)
reg = r'^\[osd\.(\d)\]$'
osd = re.compile(reg)

lines = f.readlines()
for i in range(0, len(lines)):
    osdlist = osd.findall(lines[i])
    if (osdlist):
        i=i+1
        print osdlist[0]
        hostname = lines[i].strip()
        print hostname[-8:]
'''
'''
for line in lines:
    osdlist = osd.findall(line)
    if (osdlist):
        #downloadList.append(osdlist[0])
        print osdlist
        #print f.readline()
#print len(downloadList)
#for osdid in downloadList:
    #print osdid
    '''