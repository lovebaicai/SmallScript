#!/bin/bash

FILE=url.txt

cat $FILE | while read line; do
echo $line | tr -d '\n' | redis-cli -x SADD "url" >> redis.log
echo "Success insert line: $line"
done
echo "Total number of lines in file: $i"
