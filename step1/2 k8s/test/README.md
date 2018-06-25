# docker + kubernetes

## docker
将应用程序部署到虚拟的`容器`中独立运行，与其他应用程序相互隔离，占用资源少，方便移殖(`镜像`)
### docker-windows：有图形化界面做相应的配置
* 必须用username登录，不可以用邮箱登录，否则无法从官方拉取镜像；
### docker常用指令
    docker image ls     #列出所有镜像
    docker container ls --all       #查看所有容器
    docker ps -a       #查看所有容器
    docker run **       #用指定镜像创建容器并运行

    kubectl
## kubernetes
Kubernetes是用于`自动部署`、`扩展`和`管理`**容器化应用程序**的开源系统(集群工具)。

### [ubuntu16.4安装kubernetes](https://blog.csdn.net/yan234280533/article/details/75136630)

[csdn2](https://blog.csdn.net/qq_37423198/article/details/79762687)

[官方教程](https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/)

[完整方案](https://www.cnblogs.com/RainingNight/p/using-kubeadm-to-create-a-cluster.html)

1 更新apt-get的源

    /etc/apt/sources.list
    deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted
    deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted
    deb http://mirrors.aliyun.com/ubuntu/ xenial universe
    deb http://mirrors.aliyun.com/ubuntu/ xenial-updates universe
    deb http://mirrors.aliyun.com/ubuntu/ xenial multiverse
    deb http://mirrors.aliyun.com/ubuntu/ xenial-updates multiverse
    deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse
    # kubeadm及kubernetes组件安装源
    deb https://mirrors.aliyun.com/kubernetes/apt kubernetes-xenial main


    # curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
    #国内 https://raw.githubusercontent.com/EagleChen/kubernetes_init/master/kube_apt_key.gpg 
    OK

    # echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list

    # apt-get update

2 安装docker

    # apt-get install  docker.io
    # docker version   显示版本信息
3 安装kubernetes基础组件

    # apt-get install -y kubelet kubeadm kubectl --allow-unauthenticated


4 安装kubernetes Master节点

    # 设置网络的分配地址段为：192.168.0.0/16，部署master组件
    # kubeadm init --kubernetes-version=v1.10.0 --pod-network-cidr=10.244.0.0/16

error处理
* **[ERROR Swap]: running with swap on is not supported. Please disable swap**
```
# kubelet启动参数增加–fail-swap-on=false   禁用虚拟内存
# 或$ sudo swapoff -a  #或者直接禁用,立即生效（不过重启电脑之后会还原默认设置，swap on）
或把/var/lib/etcd/文件夹清空

* pull 拉不下来问题
```
        - k8s.gcr.io/kube-apiserver-amd64:v1.10.0
		- k8s.gcr.io/kube-controller-manager-amd64:v1.10.0
		- k8s.gcr.io/kube-scheduler-amd64:v1.10.0
		- k8s.gcr.io/etcd-amd64:3.1.12 
#############
docker tag : 标记本地镜像，将其归入某一仓库。
#pull.sh
images=(kube-apiserver-amd64:v1.10.0 kube-controller-manager-amd64:v1.10.0 kube-scheduler-amd64:v1.10.0 etcd-amd64:3.1.12 kube-proxy-amd64:v1.10.0 pause-amd64:3.1)
for imageName in ${images[@]} ; do
  docker pull reg.qiniu.com/k8s/$imageName
  docker tag reg.qiniu.com/k8s/$imageName k8s.gcr.io/$imageName
  docker rmi reg.qiniu.com/k8s/$imageName
done
```

```
集群创建成功后打印输出  提示加入节点命令
```
Your Kubernetes master has initialized successfully!

To start using your cluster, you need to run the following as a regular user:
#非root运行`kubectl`
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of machines by running the following on each node
as root:

kubeadm join 192.168.11.128:6443 --token nhovtd.z93helpcllvda9yz --discovery-token-ca-cert-hash sha256:7c7e26e453c531eb52dcf5d88fc59a67bccdab22d4a59771781e19406392073a


```
* #非root运行`kubectl`
**若报错The connection to the server localhost:8080 was refused - did you specify the right host or port? 则重新执行一下语句**
```
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
```
* 浏览器中输入`https://192.168.11.128:6443/`检验是否安装成功

服务启动后会帮你创建`/etc/kubernetes/`文件夹
5 安装网络组件
```
$ sudo kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/v0.9.1/Documentation/kube-flannel.yml
```
6 kubernates 集群添加节点
安装好环境后 docker-ce,kubeadm ,kubectl,kubelet
非root 执行
```
$ sudo kubeadm join --token $MASTERTOKEN $MASTERIP:$MASTERPORT --discovery-token-ca-cert-hash sha256:$MASTERHASH
```
加入成功后可在master上查看节点
```
$ kubectl get nodes
```



## error
master reset后重新 init 报错：
**kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/v0.10.0/Documentation/kube-flannel.yml**
需要删除~/.kubd/下的cache