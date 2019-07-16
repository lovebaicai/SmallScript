# 服务器清单

- 机房环境

>## 清单列表

<br><br><br>


主机名|IP地址|端口|用途|机器所属物理机
---|---|---|---|---
sh1-arch-Lb1M-1|10.1.1.140 |10022  |外网LB-主1  |本身是物理机
sh1-arch-Lb1S-1|10.1.1.154 |10022  |外网LB-从1  |本身是物理机
sh1-arch-Lb2M-1|10.1.1.131 |10022  |外网LB-主2  |本身是物理机
sh1-arch-Lb2S-1|10.1.1.155 |10022  |外网LB-从2  |本身是物理机
lb-lan-1	   |10.1.75.4  |22	   |内网LB-1    |KVM-LB-A
lb-lan-2	   |10.1.75.5  |22	   |内网LB-2    |KVM-LB-A
lb-lan-3	   |10.1.76.4  |22	   |内网LB-3    |KVM-LB-B
lb-lan-4	   |10.1.76.5  |22	   |内网LB-4    |KVM-LB-B
lb-lan-5	   |10.1.39.4  |22     |内网LB-5    |KVM-LB-C
lb-lan-6	   |10.1.39.5  |22	   |内网LB-6    |KVM-LB-C
lvs-lan-a	   |10.1.75.3  |22	   |内网LVS-A   |KVM-LB-A
lvs-lan-b	   |10.1.76.3  |22	   |内网LVS-B   |KVM-LB-B
lvs-lan-c	   |10.1.1.200 |22	   |内网LVS-C   |本身是物理机
lvs-lan-d	   |10.1.1.211 |22	   |内网LVS-D   |本身是物理机


<br><br><br>

> - `172.16.20.72` work-rabbitmq-01 #内存节点     
> - `172.16.20.73` work-rabbitmq-02 #内存节点
> - `172.16.20.74` work-rabbitmq-03 #内存节点
> - `172.16.20.92` work-rabbitmq-04 #磁盘节点
> - `172.16.20.93` work-rabbitmq-05 #磁盘节点



### 准备工作

1.修改主机名

```
systemctl set-hostname work-rabbitmq-01
...
...
```

2.把以下信息写入到`/etc/hosts`文件中

```
172.16.20.72 node1 work-rabbitmq-01
172.16.20.73 node2 work-rabbitmq-02
172.16.20.74 node3 work-rabbitmq-03
172.16.20.92 node4 work-rabbitmq-04
172.16.20.93 node5 work-rabbitmq-05
```

### 开始部署

> 以下步骤为单节点部署步骤，请在5个节点上重复执行

1.安装erlang语言，rabbitmq依赖于erlang语言的运行环境

```
curl -s https://packagecloud.io/install/repositories/rabbitmq/erlang/script.rpm.sh | sudo bash
```

2.手动编写rabbitmq的yum源文件

vim /etc/yum.repos.d/tabbitmq.repo

插入下面内容

```
[bintray-rabbitmq-server]
name=bintray-rabbitmq-rpm
baseurl=https://dl.bintray.com/rabbitmq/rpm/rabbitmq-server/v3.7.x/el/7/
gpgcheck=0
repo_gpgcheck=0
enabled=1
```

3.安装rabbitmq服务

```
yum makecache && yum install -y rabbitmq-server
```


4.基本操作

```
#启动
systemctl start rabbitmq-server
#开机启动
systemctl enable rabbitmq-server
#查看状态
systemctl status rabbitmq-server
#重启
systemctl restart rabbitmq-server
#停止
systemctl stop rabbitmq-server
```

5.开放端口

咱们的默认防火墙和seliux都是关闭的，如果遇到没有关闭的情况，可以执行以下命令

```
#增加rabbitMQ端口：5672
sudo firewall-cmd --add-port=5672/tcp --permanent
#重新加载防火墙设置
sudo firewall-cmd --reload
```

6.添加管理配置插件（这个是web管理界面）

web界面默认监听15672端口

```
#安装web管理页面插件（先启动rabbitmq服务）：
rabbitmq-plugins enable rabbitmq_management
#开放端口
sudo firewall-cmd --add-port=15672/tcp --permanent
#重新加载防火墙配置
sudo firewall-cmd --reload
```

> 安装完成后，打开浏览器输入：`http://172.16.20.x:15672`查看rabbitmq的web界面是否可以打开。

### 组成集群

1.把node1节点上的Erlang cookie复制到其它四台节点上。如果是通过yum方式安装的rabbitmq，其位置应该是在：

```
/var/lib/rabbitmq/.erlang.cookie
```
如果找不到这个文件，那么把rabbitmq启动一下，这个文件就有了

![-w644](media/15604836742112.jpg)

其中这个Erlang cookie的值`OGALEHAVIHBZQBEUDSRS`粘贴到其它四个节点的同名文件中。

2.启动所有rabbitmq节点上的rabbitmq服务：
```
systemctl start rabbitmq-server
systemctl enable rabbitmq-server
```

3.假定我们使用node1节点当做marst界定啊，那么在剩下的其它所有节点上执行如下命令：     
`（提示：要保持rabbitmq服务运行起来的情况下，执行如下命令，如果服务没有启动起来，参见上一个操作步骤）`
```
rabbitmqctl stop_app                    # 停止rabbitmq服务
rabbitmqctl reset                       # 清空节点状态
rabbitmqctl join_cluster rabbit@node1   # node2和node1构成集群,node2必须能通过node1的主机名ping通
rabbitmqctl start_app                   # 开启rabbitmq服务
```

设置内存节点：

如果节点需要设置成内存节点，则加入集群的命令如下：

```
rabbitmqctl join_cluster --ram rabbit@node1
```

其中`–ram`指的是作为内存节点，如果不加，那就默认为内存节点。

如果节点在集群中已经是磁盘节点了，通过以下命令可以将节点改成内存节点：

```
rabbitmqctl stop_app                        # 停止rabbitmq服务
rabbitmqctl change_cluster_node_type ram    # 更改节点为内存节点
rabbitmqctl start_app                       # 开启rabbitmq服务
```

4.查看集群状态
```
rabbitmqctl cluster_status
```

### 使用NetScaler负载RabbitMQ集群

我们通过NetScaler把`172.16.20.25:5672`端口负载到下面三个节点上：

> 172.16.20.72:5672 #内存节点     
> 172.16.20.73:5672 #内存节点      
> 172.16.20.74:5672 #内存节点     

剩余的两个`磁盘节点`，我们只是加到集群中，不直接暴露给用户使用。

> 172.16.20.92:5672 #磁盘节点      
> 172.16.20.93:5672 #磁盘节点      


### 交付使用

用户通过访问：`172.16.20.25:5672`来获取rabbitmq的使用，该地址通过四层负载跳转到后面`三个rabbitmq的内存节点上`，而剩余的`两个rabbitmq磁盘节点`则用作持久化存储，之所以准备两个是为了以防万一，其中一个挂了，另一个还能坚挺的提供服务。

