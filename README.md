# docker使用
## 安装docker和docker-compose：
```shell
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo https://mirrors.ustc.edu.cn/docker-ce/linux/centos/docker-ce.repo
## 更改使用国内源，这里手动
yum makecache fast
yum install docker-ce -y

systemctl enable docker
systemctl start docker

groupadd docker
useradd guang
passwd guang
usermod -aG docker guang
```

配置docker国内镜像
vi /etc/docker/daemon.json
{
  "registry-mirrors": ["https://registry.docker-cn.com"]
}

```shell
systemctl daemon-reload
systemctl restart docker
curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```
## 运行
在当前目录运行：
docker-compose up --force-recreate --build
删除：
docker-compose down

# 注意
* 使用`gunicorn`默认值，默认监听8000端口
* `docker`和`docker-compose`都使用最新版本，`Docker version 17.09.1-ce, build 19e2cf6` 和`docker-compose version 1.18.0, build 8dd22a9`
* 程序中连接的host设置为了`db`，如果docker-compose.yml文件的server名称改变的话，docker内部的dns也会跟着改变
* flask的secretkey现在设置为一个默认值，稍后处理下
* 没有集中的配置中心，目前从环境变量中读取数据库名称，用户名密码，端口是默认的3306，连接使用utf8mb4，目前只适配了mysql，使用其他数据库，需要进一步进行设置
* 目前使用flask的默认模板引擎进行渲染，下一步考虑进行分离

# todo
* 添加测试，学习使用mock以及单元测试，对每个函数进行单元测试
* 对配置进行重新设计，以及设计一个简单的配置中心
* 添加nginx支持
* 寻找轻量级服务注册