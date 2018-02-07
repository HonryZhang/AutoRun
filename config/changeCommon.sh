#!/bin/sh
myfile=/usr/local/bin/scripts/create_cluster_scripts/bluestore/common_fun

#echo $1
#awk -v n=$lineAfter '{if($0~/\[osd\.2\]/)for(i=1;i<=n+1;i++)getline;print}' $myfile >tmp

diskfile="osd_dev="$1
echo $diskfile
awk -v  m="$diskfile" '{for(i=1;i<=NF;i++){if($i~/^osd_dev=/) $i=m}print $0}' $myfile >tmp
mv -f tmp $myfile

