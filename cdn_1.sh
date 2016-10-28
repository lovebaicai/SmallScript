#!/bin/bash
#author:nemo_chen
#version:2.0

resultFun(){
    zgrep "$1" $2 |awk 'BEGIN{sum=0};{sum +=$10};END{print sum*8/300/1000/1000}'
    }

for line in `cat log.txt`;do
    file=`echo $line | awk -F '|' '{print $1}'`
    time=`echo $line | awk -F '|' '{print $2}'`
    printf "%s is %.3f\n" $file $(resultFun $time $file)
done
