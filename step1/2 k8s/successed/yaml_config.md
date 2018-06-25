## 使用yaml文件配置 [参考](https://blog.csdn.net/phantom_111/article/details/79427144)
### YAML语法规则：
* 大小写敏感
* 使用缩进表示层级关系
* 缩进时不允许使用Tal键，只允许使用空格
* 缩进的空格数目不重要，只要相同层级的元素左侧对齐即可
* ”#” 表示注释，从这个字符一直到行尾，都会被解析器忽略
### 创建pod.yaml
```
---
apiVersion: v1
kind: Deployment
metadata:
  name: docker-demo-yaml
  labels:
    app: web
spec:
  containers:
    - name: docker-demo-yaml
      image: dennisge/docker_demo
      ports:
        - containerPort: 1226
```
* apiVersion：这个版本号需要根据安装的Kubernetes版本和资源类型进行变化，不是写死的。
* kind：此处创建的是Pod，根据实际情况，此处资源类型可以是Deployment、Job、Ingress、Service等。
* metadata：包含Pod的一些meta信息，比如名称、namespace、标签等信息。
* spec：包括一些container，storage，volume以及其他Kubernetes需要的参数，以及诸如是否在容器失败时重新启动容器的属性。可在特定Kubernetes API找到完整的Kubernetes Pod的属性。
**如果这个Pod出现了故障的话，对应的服务也就挂掉了，所以Kubernetes提供了一个Deployment的概念 ，目的是让Kubernetes去管理一组Pod的副本，也就是副本集 ，这样就能够保证一定数量的副本一直可用，不会因为某一个Pod挂掉导致整个服务挂掉。**
### 创建Deployment.yaml
**冒号后加空格**
```
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: kube100-site
spec:
  replicas: 2
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
        - name: front-end
          image: nginx
          ports:
            - containerPort: 80
        - name: flaskapp-demo
          image: jcdemo/flaskapp
          ports:
            - containerPort: 5000
```
* spec 选项定义需要两个副本，此处可以设置很多属性，例如受此Deployment影响的Pod的选择器等
* spec 选项的template其实就是对Pod对象的定义
### 执行*.yaml
```
$ kubectl create -f deploymentorpod.yaml
```