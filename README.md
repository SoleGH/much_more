# much_more
## [python](./python/README.md)
## [k8s环境搭建](./step1/2_k8s/successed/main_kubeadm_deploy_k8s_linux.md)
## [微服务](./step1/1_microservices/README.md)

### 解决不知名原因导致服务宕机，强制重启容器
```bash
# 在Dockerfile 中加入HEALTHCHECK，发现异常强制关闭进程  将`/docker-entrypoint.sh`替换为入口脚本
HEALTHCHECK --interval=60s --timeout=10s --start-period=600s --retries=3 \
  CMD curl -f http://127.0.0.1:8000/api/alive || kill $(ps aux | grep '/bin/sh /docker-entrypoint.sh' | grep -v grep | awk '{print $2}')
# 启动容器时设置`--restart=always`
```
