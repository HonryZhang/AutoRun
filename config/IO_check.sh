#! /bin/bash
sourcemd5='bad27229091370c66bdb2d788ca0505d'
while [ 1 ]
do
	for i in {1..30}
	do
	cp /root/IO_test/Ylmf_Ghost_Win7_SP1_x86_2016_1011.iso /root/IO_verify/iso.$i;
	md5sum /root/IO_verify/iso.$i>md5Tmp;
	awk '{print $1}' md5Tmp>checksum
	md5sumres=$(cat checksum)
	echo $md5sumres
	if [ "$md5sumres" = "$sourcemd5" ];then
	echo "verify mode is OK"
	else
	exit
	fi
	done
done
