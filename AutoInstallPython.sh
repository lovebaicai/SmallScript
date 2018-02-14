#!/bin/bash
#author: nemo_chen

echo "Start update development tools"
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo
yum makecache

yum update
yum groupinstall -y 'development tools'
yum install -y zlib-devel bzip2-devel openssl-devel xz-libs wget
yum install -y vim

echo "Development complate!"

echo "Start install Python2.7"

cd /opt

wget -c http://mirrors.sohu.com/python/2.7.10/Python-2.7.10.tar.xz && tar xvf Python-2.7.10.tar.xz

cd Python-2.7.10 && ./configure --prefix=/usr/local/

make && make altinstall

rm /usr/bin/python

ln -s /usr/local/bin/python2.7  /usr/bin/python

echo "Pip start install!"

curl https://bootstrap.pypa.io/get-pip.py | python -

mkdir ~/.pip

cat>~/.pip/pip.conf<<EOF
[global]
index-url = https://pypi.douban.com/simple
EOF

/usr/local/bin/pip install virtualenv -i https://pypi.douban.com/simple

echo "Pip install complate!"
echo "All tools install ok!!!!!!"

cp /usr/lib64/python2.6/lib-dynload/_sqlite3.so /usr/local/lib/python2.7/sqlite3/ 

sed -i '1s/python/python2.6/g' /usr/bin/yum

echo "Python2.7 install complate!"

echo "Start install Python3"
echo "Start update development tools"
yum install sqlite-devel -y

cd /opt
wget -c https://www.sqlite.org/2017/sqlite-autoconf-3210000.tar.gz && tar xf sqlite-autoconf-3210000.tar.gz
cd sqlite-autoconf-3210000 && ./configure --prefix=/usr/local/sqlite
make && make install

wget -c http://mirrors.sohu.com/python/3.5.3/Python-3.5.3.tar.xz && tar xvf Python-3.5.3.tar.xz
cd Python-3.5.3  
sed -i '1107,1107s/usr/local/sqlite/include' setup.py
sed -i '1108,1108s/usr/local/sqlite/include/sqlite3' setup.py
./configure --prefix=/usr/local/python3
make && make altinstall
ln -s /usr/local/python3/bin/python3.5 /usr/bin/python3
ln -s /usr/local/python3/bin/pip3.5 /usr/bin/pip3

echo "Python3.5 install complate!"
echo "All Python install done !!!!!!!!"
