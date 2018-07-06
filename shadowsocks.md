### 创建脚本  开机启动
* 创建启动脚本
```
$ sudo vim /etc/init.d/shadowsocks
#!/bin/sh
### BEGIN INIT INFO
# Provides:          shadowsocks
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: start shadowsocks 
# Description:       start shadowsocks
### END INIT INFO

start(){
    ssserver -c /etc/shadowsocks.json -d start
}

stop(){
    ssserver -c /etc/shadowsocks.json -d stop
}

case "$1" in
start)
    start
    ;;
stop)
    stop
    ;;
reload)
     stop
     start
     ;;
*)
    echo "Usage: $0 {start|reload|stop}"
    exit 1
    ;;
esac
```
* 添加可执行权限
```
$ sudo chmod +x /etc/init.d/shadowsocks
```
* 添加到开机启动
```
sudo update-rc.d shadowsocks defaults
```
* 控制命令
```
$ sudo service shadowsocks {start|reload|stop}
```
* 查看状态
```
$ systemctl status shadowsocks.service
```
