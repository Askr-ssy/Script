function install_program {
    if ! [ -x $1 ]
    then 
        apt install -y $1
    fi
}

function crlf_to_lf {
    if ! [ -f $1 ]
    then echo "file is not found" return 1
    else sed -i ':a;N;$!ba;s/\r\n/\n /g' $1
    fi
}

function install_docker {
    sudo apt-get update
    sudo apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common
    
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -         
    
    # if ! [ -x $(apt-key fingerprint 0EBFCD88) ]   # TODO 验证
    # then
    #     echo $$
    # fi

    sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $release_name \
    stable"

    sudo apt update
    sudo apt-get install docker-ce docker-ce-cli containerd.io

    sudo usermod -aG docker $(whoami)
}

function uninstall_docker {
    sudo apt-get purge docker-ce
    sudo rm -rf /var/lib/docker
}