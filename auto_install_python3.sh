#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
export PATH

# Check if user is root
if [ $(id -u) != "0" ]; then
    echo "Error: You must be root to run this script, please use root to initialization OS."
    exit 1
fi

version="3.7.5"
echo "Please enter the version number you need:"
read -p "(Default version: 3.7.5):" version
if [ "$version" = "" ];then
	version="3.7.5"
fi
name="Python"
pyfile="$name-$version.tgz"

# Check if user is root
if [ $(id -u) != "0" ]; then
    echo "Error: You must be root to run this script, please use root to install"
    exit 1
fi

yum  -y install  wget gcc gcc-c++ make openssl-devel bzip2-devel libffi-devel readline-devel zlib-devel ncurses-devel sqlite-devel autoconf bison automake zlib* fiex* libxml* ncurses-devel libmcrypt* libtool-ltdl-devel*

if [ -s $pyfile ];then
	echo -e "\033[40;31m $pyfile [found]\033[40;37m"
else
	wget https://www.python.org/ftp/python/$version/$pyfile
fi

tar zxf $pyfile

cd $name-$version
./configure --prefix=/usr/local/python3 --enable-optimizations
make altinstall

ln -s /usr/local/python3/bin/python3.7 /usr/bin/python3
ln -s /usr/local/python3/bin/pip3.7 /usr/bin/pip3

if [ -d /root/.pip ];then
	echo -e "\033[40;31m file is [found]\033[40;37m"
else
	mkdir ~/.pip

cat > ~/.pip/pip.conf <<EOF
[global]
trusted-host=mirrors.aliyun.com
index-url=https://mirrors.aliyun.com/pypi/simple/
EOF
fi

pip3 install --upgrade pip

echo -e "\nInstalled Python and pip version is ... "
python3 -V && pip3 -V

echo -e "\033[32m \nInstall Successfully! \033[0m"
