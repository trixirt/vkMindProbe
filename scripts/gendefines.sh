#!/bin/sh
# set -x
rm d.c
rm d.h
grep '^#define VK' /usr/include/vulkan/vulkan_core.h | sort -u | grep -v -e _EXT -e _KHR -e _NV -e _ARM_ -e _SEC_ -e _QCOM_ -e _GOOGLE_ -e _AMD_ -e _HUAWEI_ -e _INTEL_ -e _VALVE_ -e _NVX_ -e _IMG_ | sed -e 's/\/\/.*//' | sed -e 's/#define //' > d.txt
while read -r line; do
    M=`echo $line | awk '{ print $1 }'`
    v=`echo $line | awk '{ print $2 }'`
    echo $M $v
    echo $v | grep -e '[0-9]'
    if [ $? = 0 ]; then
	m=`echo $M | awk '{ print tolower($0) }' | sed  's/version/uint32_t version/2'`
	echo $v | grep ULL
	if [ $? = 0 ]; then
	    echo "uint64_t ${m} ();" >> d.h
	    echo "uint64_t ${m} () { return ${M}; }" >> d.c
	else
	    echo $v | grep U
	    if [ $? = 0 ]; then
		echo "uint32_t ${m} ();" >> d.h
		echo "uint32_t ${m} () { return ${M}; }" >> d.c
	    else
		echo "int ${m} ();" >> d.h
		echo "int ${m} () { return ${M}; }" >> d.c
	    fi
	fi
    fi
done < d.txt

while read -r line; do
    echo $line
done < d.txt
