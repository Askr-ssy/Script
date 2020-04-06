#!/bin/bash
source ./utils.sh

# --- 读取系统环境变量
release_name=$(lsb_release -cs)


# --- end


# --- 读取命令行参数
# export https_proxy=socks5://127.0.0.1:1080

# --- end

# --- 根据参数进行代理设置等
deb_tempdir=$(mktemp -d tempdir.XXXXXX) 

# --- end

# --- 安装 vim 等系统软件

programs="vim neofetch git guake"

for program in $programs
do
    install_program $program
done

install_docker

wget -c https://go.microsoft.com/fwlink/?LinkID=760868 -O ./$deb_tempdir/code.deb
wget -c https://d1.music.126.net/dmusic/netease-cloud-music_1.2.1_amd64_ubuntu_20190428.deb -O ./$deb_tempdir/netease.deb


# --- end

# --- 转移文件 恢复数据 处理垃圾数据

sudo rm -rf ./$deb_tempdir

# --- end

