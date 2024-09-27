```shell
mkdir -p /home/docker/proxy_pool
touch /home/docker/proxy_pool/proxy.txt
chmod 777 /home/docker/proxy_pool
```

```shell
docker run -d \
  --name proxy_pool \
  -p 5010:5010 \
  -v /home/docker/proxy_pool:/app/textProxy \
  -e DB_CONN=redis://:root@192.168.0.234:6379/0 \
  registry.cn-hangzhou.aliyuncs.com/nacl-public/proxy_pool:v1.0
```