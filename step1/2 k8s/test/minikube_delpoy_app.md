# [链接](https://github.com/gedennis/node-tribe-blog/issues/5)


https://www.jianshu.com/p/a552076d4fe3


linux 卡在event第三行
![win执行run结果](../images/kubectl_run_successed_win.png)


### 发布服务
```
kubectl expose deployment/<deployment name> --type=NodePort --port 1226
```
### 获取服务url
```
minikube service <deployment name>
```
![访问服务](../images/get_server_url.png)
