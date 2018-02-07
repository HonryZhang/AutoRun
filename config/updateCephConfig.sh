#!/bin/sh
myfile=/etc/ceph/ceph.conf
lineAfter=6
#echo $1
#awk -v n=$lineAfter '{if($0~/\[osd\.2\]/)for(i=1;i<=n+1;i++)getline;print}' $myfile >tmp
awk -v  m="$1" '{if($0==m)for(i=1;i<=6;i++)getline;print}' $myfile >tmp
mv -f tmp $myfile
