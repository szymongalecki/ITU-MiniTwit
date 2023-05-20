# Replication and Infrastructure as a Service
### Author: Dagmara Przygocka

## Replication
The team decided to scale the project by implementing a high-availability setup with a hot and standby server for your ITU-MiniTwit application. The set up includes having two replicas of our MiniTwit application server where only one is ever active at a time. To implement it we followed Digital Ocean tutorial: How To Set Up Highly Available Web Servers with Keepalived and Reserved IPs on Ubuntu 14.04 (https://www.digitalocean.com/community/tutorials/how-to-set-up-highly-available-web-servers-with-keepalived-and-reserved-ips-on-ubuntu-14-04).

The current status of MiniTwit application includes running database service as a part of Docker stack. Each server has its own stack deployed which includes volumes where the data are kept. The result of this implementation is that no matter which approach we will take, either Docker Swarm or High Availability setup with a hot and standby server, we will have the problem with data consistency. The reason why we chose the second approach is due to our Digital Ocean account which allows only 3 droplets where one was already taken by the initially deployed server. In order to create replicas we would need to take down the current server which would result in loss of volumes we collected when the simulation was running. Future improvements could include:
- Separating databases form the stack so all replicas could have one source of data.
- Increasing Digital Ocean account resources so we could have more than 3 droplets.
- Migrating the data from the initial server and deploying the replicas.
- Research why keepalived is not executing master.sh script even though it registers the change of state from MASTER to BACKUP. (for now we have a workaround where we check if the state is master and than we check if it has assigned reserved ip, to other option is to ssh into the server stop keepalived and start it with command: "keepalived -S 7 -f /etc/keepalived/keepalived.conf -D -n". The command when run in vagrant works but freezes the execution and the file can not finish.)

The current implementation involves 3 servers where:
- The initial server containing the data collected during the simulation.
- Other two are the result of implementing the high availability setup with a hot and standby server.

## Infrastructure setup

### Vagrantfile (in folder hot_server)
In the Vagrantfile we create two virtual machines which have their own setup. The setup is mostly the same as it is described in virtualization_&_deployment_choice.md. The additions are as following to the main machine:
- Set private network and assign ip address to: "10.114.0.4"
- Add to additional environment variables for the machine: RESERVED_IP and DO_TOKEN
- Run curl request to get the droplet id
- Assign the reserved IP address to the droplet virtual machine
- Create keepalived folder
- Copy keepalived.conf file from host machine to the guest machine from folder first
- Run the common script
To the backup:
- Set private network and assign ip address to: "10.114.0.5"
- Add to additional environment variables for the machine: RESERVED_IP and DO_TOKEN
- Create keepalived folder
- Copy keepalived.conf file from host machine to the guest machine from folder second
- Run the common script
 The machines share a script that runs the same steps for both machines. The script:
- Updates the package lists for available software packages
- Instals (with yes to any questions) keepalived package
- Gets the assign-ip script , used for reassigning the reserved ip from main to backup server.
- Instals (with yes to any questions) python3 package
- Copies the master.sh form host server to /etc/keepalived/master.sh
- Changes executable permissions for master.sh and check_containers.sh
- Starts keepalived service
- Starts the docker-compose file for the machine
The rest of the script is described in a file called virtualization_&_deployment_choice.md. 

The keepalived configuration will run check_container.sh script which checks if the number of containers in docker are equal to 10. If the script exists with 1 it means that the machine has to go into failure state and the backup server takes over the reserved IP. The failure of check_contaners.sh script fires up the master.sh script in which we check if the machine has already assigned reserved IP, if not it runs the assign-ip script.

You can find the Vagrantfile and scripts under the hot_server folder.

### Environment variables:
In order to run the Vagrantfile which will create the infrastructure with high availability setup with a hot and standby server we need to create the following environmental variables:
- DIGITAL_OCEAN_TOKEN
- DOCKER_USERNAME
- DOCKER_PASSWORD
- RESERVED_IP
Except for the variables, remember to have the ssh token set up in Digital Ocean.

### Run the setup
- vagrant up --provider=digital_ocean

## Limitations and Future Steps:
- To implement the infrastructure we require the digital ocean account to have an unassigned reserved ip address. The reason is that in the Vagrant file we are able to create and assign a new reserved ip address to a virtual machine but we are not able to pass the newly created IP address to the second virtual machine created as a backup. The reserved IP is necessary for the keepalived service to work properly and reassign the reserved IPaddress from first server to backup server in case of failure.
- The private IP addresses assigned to machines also have to be known prior to the Vagrant setup. The reason is the same as mentioned above.
- The data are not exchanged between the virtual machines which will result in data inconsistency when switching from main to backup server.
- The private IP for the virtual machines are hard coded. To change them we need to go to keepalived configuration for both of the servers.
- Both virtual machines are running with root privileges. In order to decrease security risks we could create new users who have appropriate privileges (could use sudo) to run the setup.

## Rolling Update
The pipeline for rolling updates is very similar to the one described in the file called CI_CD_choice.md. The changes made to enforce the rolling updates are:
- Adding backup server to with the changes will be deployed 
- Check if the services are built and running after the deployment to the main server. If they are running then start deployment of the second server.
The chech invokes check_containers.sh which will indicate if all 10 containers are up and running within 300 s. If the check fails the second server is not updated.
The new github action pipeline is in the file called rolling-updates.yml.
