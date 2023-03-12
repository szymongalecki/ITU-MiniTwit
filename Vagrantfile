# -*- mode: ruby -*-
# vi: set ft=ruby :
#Vagrant configuration version and initializes the configuration block
Vagrant.configure("2") do |config|
  #sets the base box image that will be used to create the virtual machine
  config.vm.box = 'digital_ocean'
  # URL of the base box image.
  config.vm.box_url = "https://github.com/devopsgroup-io/vagrant-digitalocean/raw/master/box/digital_ocean.box"
  #path to the private SSH key that will be used to authenticate with the virtual machine
  #pubm key is set in digital ocean
  config.ssh.private_key_path = '~/.ssh/do_ssh_key'

  #reates a synced folder between the host machine and the virtual machine, 
  #where files can be shared. In this case, the "remote_files" folder on the host machine will be synced
  # with the "/minitwit" folder on the virtual machine using the "rsync" type
  # TO DO CRETAE REMOTE FILES FOLDER WITH DOCKER CREDENTIALS AND COMPOSE TO RUN
  config.vm.synced_folder "remote_files", "/minitwit", type: "rsync"
  #This line creates a synced folder between the host machine and the virtual machine, but it is disabled in this case.
  config.vm.synced_folder '.', '/vagrant', disabled: true
  #defines the virtual machine with the name "minitwit" and
  # sets it as the primary machine. It also initializes the server block.
  config.vm.define "minitwit", primary: true do |server|
#specifies that the virtual machine will be created on the DigitalOcean cloud platform and initializes the provider block.
    server.vm.provider :digital_ocean do |provider|
      #specifies the name of the SSH key that will be used to authenticate with the DigitalOcean virtual machine.
      provider.ssh_key_name = "do_ssh_key"
      # line specifies the DigitalOcean API token that will be used to create and manage the virtual machine.
      provider.token = ENV["DIGITAL_OCEAN_TOKEN"]
      #specifies the base image that will be used to create the virtual machine.
      provider.image = 'ubuntu-20-04-x64'
      #specifies the region where the virtual machine will be created.
      provider.region = 'fra1'
      # specifies the size of the virtual machine.
      # "s": This is the size class, which typically refers to the level of resources allocated to the instance.
      # "1vcpu": This specifies the number of virtual CPUs allocated to the instance, which in this case is one.
      # "1gb": This specifies the amount of memory allocated to the instance, which in this case is one gigabyte.
      provider.size = 's-1vcpu-1gb'
    end
    # sets the hostname of the virtual machine.
    server.vm.hostname = "minitwit-ci-server"
    # runs a shell script to set the environment variable DOCKER_USERNAME.
    server.vm.provision "shell", inline: 'echo "export DOCKER_USERNAME=' + "'" + ENV["DOCKER_USERNAME"] + "'" + '" >> ~/.bash_profile'
    # runs a shell script to set the environment variable DOCKER_PASSWORD.
    server.vm.provision "shell", inline: 'echo "export DOCKER_PASSWORD=' + "'" + ENV["DOCKER_PASSWORD"] + "'" + '" >> ~/.bash_profile'
    
    #runs a multiline shell script that installs Docker,
    # Docker Compose, and Make, and configures the virtual machine for running the Minitwit application.
    server.vm.provision "shell", inline: <<-SHELL
    
    # Install docker and docker-compose
    sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
    apt-cache policy docker-ce
    sudo apt install -y docker-ce
    sudo systemctl status docker
    sudo usermod -aG docker ${USER}
    sudo apt install -y docker-compose
    

    # Install make
    sudo apt-get install -y make
    
    echo -e "\nVerifying that docker works ...\n"
    docker run --rm hello-world
    docker rmi hello-world

    echo -e "\nOpening port for minitwit ...\n"
    ufw allow 5000 && \
    ufw allow 8000 && \
    ufw allow 22/tcp

    echo ". $HOME/.bashrc" >> $HOME/.bash_profile

    echo -e "\nConfiguring credentials as environment variables...\n"

    source $HOME/.bash_profile

    echo -e "\nSelecting Minitwit Folder as default folder when you ssh into the server...\n"
    echo "cd /minitwit" >> ~/.bash_profile

    chmod +x /minitwit/deploy.sh
    
    echo -e "\nVagrant setup done ..."
    echo -e "minitwit will later be accessible at http://$(hostname -I | awk '{print $1}'):8000"
    SHELL
  end
end
