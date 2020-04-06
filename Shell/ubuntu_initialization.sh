#!/bin/bash
source ./utils.sh

# --- 读取系统环境变量
release_name=$(lsb_release -cs)
# TODO 设置国外源或者国内源 修改文件

# --- end


# --- 读取命令行参数
# TODO 是否代理

# --- end

# --- 根据参数进行代理设置等
# export https_proxy=socks5://127.0.0.1:1080
deb_tempdir=$(mktemp -d tempdir.XXXXXX) 
# TODO 设置日志出处

# --- end

# --- 安装 vim 等系统软件
sudo apt update 
sudo apt -y upgrade
programs="vim neofetch git guake"

for program in $programs
do
    install_program $program
done

install_docker
# TODO 安装 firefox chromium-browser telegram qbittorrent calibre mariadb redis-server postman vpn

wget -c https://go.microsoft.com/fwlink/?LinkID=760868 -O ./$deb_tempdir/code.deb
wget -c https://d1.music.126.net/dmusic/netease-cloud-music_1.2.1_amd64_ubuntu_20190428.deb -O ./$deb_tempdir/netease.deb

# TODO 循环安装deb_tempdir 目录下的deb文件

# --- end

# --- 转移文件 恢复数据 处理垃圾数据
# TODO 恢复国内源或者国外源

sudo rm -rf ./$deb_tempdir

# --- end