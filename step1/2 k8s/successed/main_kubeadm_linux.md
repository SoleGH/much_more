## kubeadm,kubectl and kubelet 安装
### [官网推荐](https://kubernetes.io/docs/tasks/tools/install-kubeadm/)
```
apt-get update && apt-get install -y apt-transport-https curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update
apt-get install -y kubelet kubeadm kubectl
```
### 网络问题
* 解决方案：使用proxychains:
```
$ proxychains apt-get curl ...
$ proxychains apt-get update
```
### 问题二：使用proxychains依旧无法添加秘钥
* 报错内容：
```
gpg: no valid OpenPGP data found.
```
* 解决方案：
```
#先将秘钥文件下载到本地
$ proxychains curl -O https://packages.cloud.google.com/apt/doc/apt-key.gpg
# 添加下载在当前目录的秘钥文件(apt-key.gpg为前一条指令下载的文件)
$ apt-key add apt-key.gpg
OK
```
### 安装docker
```
$ apt-get install  docker.io
$ docker version   显示版本信息
```
### 安装kubernetes Master节点
```
$ kubeadm init --kubernetes-version=v1.11.0 --pod-network-cidr=10.244.0.0/16
```
* 加`--kubernetes-version`参数执行，如果不加则报错（还是网络问题，proxychains无效）：
```
unable to get URL "https://dl.k8s.io/release/stable-1.11.txt": Get https://storage.googleapis.com/kubernetes-release/release/stable-1.11.txt: read tcp 172.16.3.170:60992->172.217.24.16:443: read: connection reset by peer
```
* kubelet 关闭swap
```
#/etc/systemd/system/kubelet.service.d/10-kubeadm.conf
Environment="KUBELET_SWAP_ARGS=--fail-swap-on=false"
ExecStart=+ $KUBELET_SWAP_ARGS
```
* 修改`/etc/default/kubelet`:
```
KUBELET_EXTRA_ARGS=--pod-infra-container-image=registry.cn-hangzhou.aliyuncs.com/yangbf/pause-amd64
```
* 修改`/etc/systemd/system/kubelet.service.d/10-kubeadm.conf`
```
# vim /etc/systemd/system/kubelet.service.d/10-kubeadm.conf

Environment="KUBELET_INFRA_IMAGE=--pod-infra-container-image=docker.cinyi.com:443/senyint/pause-amd64:3.1"
ExecStart=+ $KUBELET_INFRA_IMAGE
```
* 统一[cgroup](https://github.com/SoleGH/much_more/issues/10)
* kubeadm init 配置
```
#k8s_ini.conf
apiVersion: kubeadm.k8s.io/v1alpha1
kind: MasterConfiguration
api:
  advertiseAddress: 0.0.0.0
networking:
  podSubnet: 10.244.0.0/16
etcd:
  image: soleyang/etcd-amd64:3.2.18
kubernetesVersion: v1.11.0
imageRepository: soleyang
```
* 初始化(确保kubelet状态为active)
```
# 查看kubelet状态
$ systemctl status kubelet
$ swapoff -a && kubeadm init --config k8s_init.conf 
```
* 初始化成功
```
Your Kubernetes master has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of machines by running the following on each node
as root:

  kubeadm join 172.16.3.170:6443 --token 4hlb1s.q7ovyg193mdxlkye --discovery-token-ca-cert-hash sha256:5d46438a6ebcf076eb2d793531062fd394aeb3bececcf1a562a247a02bae0a21


``