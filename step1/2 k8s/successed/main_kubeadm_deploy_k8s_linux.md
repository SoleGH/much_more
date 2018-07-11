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
## 部署kubernetes Master节点
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

  #执行前删除原有配置文件，避免发生配置文件原因引发无法链接服务器问题
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of machines by running the following on each node
as root:

  kubeadm join 172.16.3.170:6443 --token ff8o8p.pidb75sgqt87givu --discovery-token-ca-cert-hash sha256:f1f320c210ca43ca196b2b8a9c53013950fa48d994c4ec750b59a8703a33e988
```
### 安装网络组件
```
#对应podSubnet: 10.244.0.0/16
$ kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/v0.10.0/Documentation/kube-flannel.yml
```
### 相关指令
```
$ kubeadm token list
$ kubectl get nodes
$ kubectl get pod -o wide #查看服务运行在哪个节点
```
### 添加子节点
* 安装环境 kubeadm kubelet kubectl docker
* 配置kubelet(同masker,不确定是否必要，不确定node镜像是通过master获取还是直接通过网络，如果是网络则必须配置，待测试)
* 使用`kubeadm init`生成的`kubeadm join --token......`添加节点
```
root@yangbf-VirtualBox:/etc/default# kubeadm join 172.16.3.170:6443 --token ff8o8p.pidb75sgqt87givu --discovery-token-ca-cert-hash sha256:f1f320c210ca43ca196b2b8a9c53013950fa48d994c4ec750b59a8703a33e988
[preflight] running pre-flight checks
I0711 10:05:46.739716   16803 kernel_validator.go:81] Validating kernel version
I0711 10:05:46.739790   16803 kernel_validator.go:96] Validating kernel config
[discovery] Trying to connect to API Server "172.16.3.170:6443"
[discovery] Created cluster-info discovery client, requesting info from "https://172.16.3.170:6443"
[discovery] Requesting info from "https://172.16.3.170:6443" again to validate TLS against the pinned public key
[discovery] Cluster info signature and contents are valid and TLS certificate validates against pinned roots, will use API Server "172.16.3.170:6443"
[discovery] Successfully established connection with API Server "172.16.3.170:6443"
[kubelet] Downloading configuration for the kubelet from the "kubelet-config-1.11" ConfigMap in the kube-system namespace
[kubelet] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[preflight] Activating the kubelet service
[tlsbootstrap] Waiting for the kubelet to perform the TLS Bootstrap...
[patchnode] Uploading the CRI Socket information "/var/run/dockershim.sock" to the Node API object "yangbf-virtualbox" as an annotation

This node has joined the cluster:
* Certificate signing request was sent to master and a response
  was received.
* The Kubelet was informed of the new secure connection details.

Run 'kubectl get nodes' on the master to see this node join the cluster.

```
* 在master查看新增节点(获取镜像需要时间，等一会)
```
$ kubectl get nodes
```
### [部署应用](./deploy_app.md)
