#!/bin/bash

set -e

#Add the parameters in this endurance script
while [ $# -gt 0 ] ; do
    case $1 in
           --write) shift 1; io_write="$1" ;;
           --read) io_read="$1" ;;
	   --rw) io_rw="$1";;	
             *) echo "You can add the params with 'write','read' or 'ro'."; exit 1 ;;
    esac
    shift 1
done

#Send the IO consistently and continually with different types
#fio 8k_randwrite.fio
#fio 8k_randread.fio

#Run the normal ceph operation in long term  
START_DATE=`date +%s`
echo "START_DATE is $START_DATE ===================="
END_DATE=$(($START_DATE + 2*20*60*60))
#END_DATE=$(($START_DATE + 6*60))

echo "END_DATE is $END_DATE =================="

while (((`date +%s`) < $END_DATE))
do
echo "Write IO with 1M block size ===================="
fio 1M_seqwrite.fio
echo "Write IO with 8K block size ===================="
fio 8k_randwrite.fio
echo "Read IO with 8K block size ===================="
fio 8k_randread.fio

for ((i=100; i<150; i++));
do

echo "create pool pool$i ===================="
ceph osd pool create pool$i 256
echo "create image pool$i-image on pool$i ===================="
rbd create pool$i-image --size 100G --pool pool$i
echo "create snap on image pool$i-image ===================="
rbd -p pool$i snap create --snap pool$i-snap pool$i-image
echo "list snap$i ===================="
rbd snap ls pool$i/pool$i-image
echo "resize pool$i-image size ===================="
rbd resize --image pool$i-image -p pool$i --size 150G
echo "rename pool$i name ===================="
rbd snap protect pool$i/pool$i-image@pool$i-snap 
echo "Clone snap pool$i-snap ===================="
rbd clone pool$i/pool$i-image@pool$i-snap pool$i/new-pool$i-image
echo "List children on snap pool$i-snap ===================="
rbd children pool$i/pool$i-image@pool$i-snap
echo "Create clone on snap pool$i-snap ===================="
rbd -p pool$i snap create --snap new-pool$i-snap new-pool$i-image
echo "List clone on snap pool$i-snap ===================="
rbd snap ls pool$i/new-pool$i-image
echo "Delete clone on snap pool$i-snap ===================="
rbd snap rm pool$i/new-pool$i-image@new-pool$i-snap
echo "Delete children on snap pool$i-snap ===================="
rbd remove --pool pool$i --image new-pool$i-image
echo "Unprotect snap pool$i-snap ===================="
rbd snap unprotect pool$i/pool$i-image@pool$i-snap
echo "remove snap$i ===================="
rbd snap rm pool$i/pool$i-image@pool$i-snap
echo "remove pool$i-image ===================="
rbd remove --pool pool$i --image pool$i-image
echo "remove pool$i-new ===================="
ceph osd pool delete pool$i pool$i --yes-i-really-really-mean-it
echo "check ceph status and osd tree status ===================="
ceph -s
ceph osd tree
echo "RW IO with 8K block size ===================="
fio 8k_randwr.fio

done
echo "Read IO with 1M block size ===================="
fio 1M_seqread.fio
done
