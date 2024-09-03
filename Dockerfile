FROM python:3.6-alpine

# 设置工作路径
WORKDIR /app

# 复制项目
COPY . .

# 设置镜像源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

# 设置时区
RUN apk add -U tzdata && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && apk del tzdata

# 安装运行环境
RUN apk add musl-dev gcc libxml2-dev libxslt-dev

# 安装python组件
RUN pip install --no-cache-dir -r requirements.txt

# 删除无用环境
RUN apk del gcc musl-dev

# 暴露端口
EXPOSE 5010

# 运行app
ENTRYPOINT [ "sh", "start.sh" ]
