#!/bin/bash
#read -p 'Please input your filename: ' file
#read -p 'Please input your time: ' time
#echo $time
#echo $file
for file in ./*.gz
do
	for speed in $(zgrep '2016:23:2[5-9]' $file | awk 'BEGIN{sum=0};{sum +=$10};END{print sum*8/300/1000/1000}')
	do 
	echo $speed
	done
done
