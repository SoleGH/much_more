# [用kubeadm创建master](https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/#version-skew-policy)
## 确定kubeadm已安装，并更新kubeadm
```
$ apt-get update && apt-get upgrade
```
## 初始化master （kubeadm init <args>）
* 初始化master
    * --pod-network-cidr (必选)节点组[网络插件](https://kubernetes.io/docs/setup/independent/create-cluster-kubeadm/#pod-network) ,保障pods间的通讯
    ```
    kubeadm init –-kubernetes-version=v1.10.0 --pod-network-cidr=10.244.0.0/16  #制定网络插件为flannel
    ```
* 安装网络组件flannel（官方提供的pod-network的一个）：
```
$ kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/v0.10.0/Documentation/kube-flannel.yml
```

* 检测插件是否运行，若运行则 `kube-dns pod` 会自动运行；
    ```
    $ kubectl get pods --all-namespaces
    ```

## 添加子节点
* 根据部署master成功后打印内容添加即可