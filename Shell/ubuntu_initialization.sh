#!/bin/bash

# --- 读取系统环境变量

release_name=$(lsb_release -cs)

# --- end

# --- 读取命令行参数
export https_proxy=socks5://127.0.0.1:1080

# --- end

# --- 根据参数进行代理设置等

# --- end

# --- 安装 vim 等系统软件
apt install vim
# --- end

# --- 安装 用户软件

# --- end

# --- 转移文件 恢复数据

# --- end