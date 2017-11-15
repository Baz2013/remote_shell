# remote_shell
## 脚本功能
1. 在远程主机上执行命令
2. 拷贝文件到远程主机的指定目录下
3. 在远程主机上执行脚本

## 使用方法
1. 在当前目录下的rcm.conf配置文件中配置主机组，如：
  ```commandline
  [test_redis_hosts]
  10.190.xx.1
  10.190.xx.2
  10.190.xx.3
  ```
2. 执行命令
  ```python
   python main.py -m command -u redis -p redis_passwd -d "test_redis_hosts" -c "ps -ef|grep redis"
  ```
  
  -m 模式，可选模式有command/copy/shell 分别对应执行命令/拷贝文件/执行脚本
  -u 用户名
  -p 密码
  -d 主机组
  -c 要执行的命令
  
  copy文件
  ```python
   python main.py -m copy -u user -p passwd -d test_redis_hosts -c "src=./autoacct_new_logger.config dest=~/logstash-2.3.4/config"
  ```
  
  shell脚本
  ```python
   python main.py -m shell -u user -p passwd -d test_redis_hosts -c "src=./change_bashrc_2.sh dest=~/user"
  ```
  
## 依赖
  该脚本依赖的第三方库有
  ```python
   pexpect 3.1
  ```
  
