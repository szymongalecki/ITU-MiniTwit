# -*- mode: ruby -*-
# vi: set ft=ruby :

$ip_file = "db_ip.txt"

Vagrant.configure("2") do |config|
    config.vm.box = 'xtangle/pop_os-20.04'
    # config.vm.box_url = "https://iso.pop-os.org/22.04/amd64/intel/22/pop-os_22.04_amd64_intel_22.iso"
    # config.ssh.private_key_path = "~/.ssh/id_rsa"
    config.ssh.forward_agent = true
    config.vm.network "forwarded_port", guest: 80, host: 8080
    config.vm.synced_folder ".", "/vagrant", type: "rsync"
    config.ssh.username = 'vagrant'
    config.ssh.password = 'vagrant'
    config.ssh.insert_key = 'true'
    config.vm.provider "virtualbox" do |vb|
        vb.gui = true
        vb.memory = "4096"
      end

    config.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt install -y python3-pip
      pip install --upgrade pip
      pip install django
      git clone https://github.com/szymongalecki/ITU-MiniTwit.git
      cd ITU-MiniTwit/ITU_MiniTwit
      python3 manager.py runserver
    SHELL
end