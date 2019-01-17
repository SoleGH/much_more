# ubuntu 部署hadoop
## 参考
* [digitalocean](https://www.digitalocean.com/community/tutorials/how-to-install-hadoop-in-stand-alone-mode-on-ubuntu-16-04)
* [纯洁的微笑](http://www.ityouknow.com/hadoop/2017/07/24/hadoop-cluster-setup.html)

## 环境
* ubuntu 16.4
* java 1.8
* hadoop 2.7.7

## 部署准备
### 设置主机名和域名映射
* 设置主机名,修改 `/etc/hostname`,将主机名改为**hadoop-master**
* 添加域名映射,修改 `/etc/hosts`
```
.
.
.
192.168.0.180 hadoop-master
192.168.0.181 hadoop-slave1
192.168.0.182 hadoop-slave2
```
### 安装jdk
* 更新软件包列表
```
$ sudo apt-get update
```
* 安装jdk
```
$ sudo apt-get install openjdk-8-jdk
```
* 查看是否安装成功
```
$ java -version
openjdk version "1.8.0_191"
OpenJDK Runtime Environment (build 1.8.0_191-8u191-b12-0ubuntu0.16.04.1-b12)
OpenJDK 64-Bit Server VM (build 25.191-b12, mixed mode)
```
### 安装sshd
### 设置本机ssh无密码登录
* 生成秘钥
```
$ ssh-keygen -t rsa
```
* 将公钥添加加到`authorized_keys`文件
```bash
$ cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
```
* 修改权限
```
$ chmod 600 .ssh/authorized_keys
```
* 验证本机无密码登录
```bash
$ ssh hadoop-master
# 连接成功显示
Welcome to Ubuntu 16.04.5 LTS (GNU/Linux 4.4.0-31-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

61 packages can be updated.
25 updates are security updates.

New release '18.04.1 LTS' available.
Run 'do-release-upgrade' to upgrade to it.

Last login: Wed Jan 16 23:18:19 2019 from 192.168.0.180

```

## 下载/校验包完整性 hadoop
### [官网下载](http://hadoop.apache.org/releases.html)
* 下载[hadoop-2.7.7.tar.gz](https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-2.7.7/hadoop-2.7.7.tar.gz)（**注意不是hadoop-2.7.7.src.tar.gz**）
* (可不操作)下载md5校验文件[hadoop-2.7.7.tar.gz.mds](https://dist.apache.org/repos/dist/release/hadoop/common/hadoop-2.7.7/hadoop-2.7.7.tar.gz.mds)
* （不校验可跳过）运行指定 对比sha256 是否相同，相同则无篡改
```bash
$ shasum -a 256 hadoop-2.7.7.tar.gz 
d129d08a2c9dafec32855a376cbd2ab90c6a42790898cabbac6be4d29f9c2026  hadoop-2.7.7.tar.gz

$ cat hadoop-2.7.7.tar.gz.mds
hadoop-2.7.7.tar.gz:    MD5 = CC 2F 01 9F 2A 41 45 8D  F8 43 0C 44 8B B9 F7 60
hadoop-2.7.7.tar.gz:   SHA1 = DA60 1BF9 79CB 63DB 78EC  F85A 617B 4FF4 B265 5D23
hadoop-2.7.7.tar.gz: RMD160 = 0C91 94F1 C22A DB54 0B23  4841 4B80 2074 D4AF 56A2
hadoop-2.7.7.tar.gz: SHA224 = 83D70DC7 D579DDB4 3B3BA00D BA1A9695 2D73A0A4
                              9286F404 219186AB
hadoop-2.7.7.tar.gz: SHA256 = D129D08A 2C9DAFEC 32855A37 6CBD2AB9 0C6A4279
                              0898CABB AC6BE4D2 9F9C2026
hadoop-2.7.7.tar.gz: SHA384 = 7FD6F49A F16D4324 988B41B6 46C690B6 AFBABB24
                              BA18C123 571AE4E2 277495EA 31335245 BF767707
                              ED44BBAF 9A978F3F
hadoop-2.7.7.tar.gz: SHA512 = 17C89172 11DD4C25 F78BF601 30A390F9 E273B014
                              9737094E 45F4AE5C 917B1174 B97EB908 18C5DF06
                              8E607835 12012628 1BCC0751 4F38BD7F D3CB8E9D
                              3DB1BDDE

```
### 部署
### 解压并移动文件到`/usr/local/hadoop`目录
``` bash
# 解压
$ tar -axvf hadoop-2.7.7.tar.gz
# 移动
$ sudo mv ./hadoop-2.7.7 /usr/local/hadoop
```
### hadoop配置java路径（可不配，默认同系统）
```bash
# 修改 /usr/local/hadoop/etc/hadoop/hadoop-env.sh
# export JAVA_HOME=${JAVA_HOME}
# export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre/
export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")
```
### 配置hadoop-master的hadoop环境变量

* 配置环境变量，修改配置文件`/etc/profile`
```
$ vi /etc/profile
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin 
```
* 使配置生效
```
$ source /etc/profile
```

-------------------------------
### 修改`/usr/local/hadoop/etc/hadoop`下的配置文件
* 配置`core-site.xml`

配置节点 | 说明
--------|---------
fs.default.name | 指定NameNode的IP地址和端口号
hadoop.tmp.dir | 指定hadoop数据存储的临时文件夹

**如没有配置hadoop.tmp.dir参数，此时系统默认的临时目录为：/tmp/hadoo-hadoop。而这个目录在每次重启后都会被删除，必须重新执行format才行，否则会出错。**
```xml
<configuration>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>file:/usr/local/hadoop/tmp</value>
        <description>Abase for other temporary directories.</description>
    </property>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://hadoop-master:9000</value>
    </property>
</configuration>
```
* 配置`hdfs-site.xml`

配置节点 | 说明
--------|---------
dfs.replication | 指定HDFS的备份因子为3
dfs.name.dir | 指定namenode节点的文件存储目录
dfs.data.dir | 指定datanode节点的文件存储目录
```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>3</value>
    </property>
    <property>
        <name>dfs.name.dir</name>
        <value>/usr/local/hadoop/hdfs/name</value>
    </property>
    <property>
        <name>dfs.data.dir</name>
        <value>/usr/local/hadoop/hdfs/data</value>
    </property>
</configuration>
```
* 配置`mapred-site.xml`

**拷贝mapred-site.xml.template为mapred-site.xml，再进行修改**
```
$ cp /usr/local/hadoop/etc/hadoop/mapred-site.xml.template /usr/local/hadoop/etc/hadoop/mapred-site.xml  
```
修改`mapred-side.xml`为
```xml
<configuration>
  <property>
      <name>mapreduce.framework.name</name>
      <value>yarn</value>
  </property>
   <property>
      <name>mapred.job.tracker</name>
      <value>http://hadoop-master:9001</value>
  </property>
</configuration>
```
* 配置`yarn-site.xml`
```xml
<configuration>
<!-- Site specific YARN configuration properties -->
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>hadoop-master</value>
    </property>
</configuration>
```
* 配置`masters`文件

**说明**：该文件指定namenode节点所在的服务器机器。删除localhost，添加namenode节点的主机名hadoop-master；不建议使用IP地址，因为IP地址可能会变化，但是主机名一般不会变化。
```bash
$ vi /usr/local/hadoop/etc/hadoop/masters
# localhost
# 不建议使用IP地址，因为IP地址可能会变化，需要在/etc/hosts 中设置域名映射
hadoop-master
```
* 配置slaves文件（Master主机特有）

**说明**： 该文件指定哪些服务器节点是datanode节点。
```bash
$ vi /usr/local/hadoop/etc/hadoop/slaves
# 内容
hadoop-slave1
hadoop-slave2
hadoop-slave3
```
### 配置hadoop-slave的hadoop环境
**示范slave1,添加更多节点操作相同**
* 复制hadoop-master的hadoop文件夹到hadoop-slave1节点
```
scp -r /usr/local/hadoop hadoop-slave1:/usr/local/
```
* 删除hadoop-slaves1,文件夹下的slaves文件
```
$ rm -rf /usr/local/hadoop/etc/hadoop/slaves
```
* 配置环境变量
```bash
$ vi /etc/profile
# 内容
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin

# 使环境变量生效；
$ source /etc/profile
```

### 启动集群
* 格式化HDFS文件系统,进入master的~/hadoop目录，执行:
```bash
# 格式化namenode，第一次启动服务前执行的操作，以后不需要执行
$ bin/hadoop namenode -format
```

* 启动hadoop：
```bash
$ sbin/start-all.sh
**说明**：
```
* 使用jps命令查看运行情况
**说明**：jps命令可以查看HDFS文件管理系统、MapReduce服务是否启动成功，但是无法查看到Hadoop整个集群的运行状态。
```
$ jps
```
* 命令查看Hadoop集群的状态
```bash
# 查看节点运行状态，HDFS的容量使用情况，节点的硬盘使用情况。
$ hadoop dfsadmin -report
DEPRECATED: Use of this script to execute hdfs command is deprecated.
Instead use the hdfs command for it.

Configured Capacity: 19945680896 (18.58 GB)
Present Capacity: 13517348864 (12.59 GB)
DFS Remaining: 13517320192 (12.59 GB)
DFS Used: 28672 (28 KB)
DFS Used%: 0.00%
Under replicated blocks: 0
Blocks with corrupt replicas: 0
Missing blocks: 0
Missing blocks (with replication factor 1): 0

-------------------------------------------------
Live datanodes (1):

Name: 192.168.0.180:50010 (hadoop-master)
Hostname: hadoop-master
Decommission Status : Normal
Configured Capacity: 19945680896 (18.58 GB)
DFS Used: 28672 (28 KB)
Non DFS Used: 5391552512 (5.02 GB)
DFS Remaining: 13517320192 (12.59 GB)
DFS Used%: 0.00%
DFS Remaining%: 67.77%
Configured Cache Capacity: 0 (0 B)
Cache Used: 0 (0 B)
Cache Remaining: 0 (0 B)
Cache Used%: 100.00%
Cache Remaining%: 0.00%
Xceivers: 1
Last contact: Thu Jan 17 03:14:23 PST 2019

```
* hadoop 重启
```
$ sbin/stop-all.sh
$ sbin/start-all.sh
```




