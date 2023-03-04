# Export env variables (set ELK_DIR to directory where this script is located)
# directory for the setup_elk.sh script
export ELK_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# check the user
export ELK_USER="$( whoami )"

#  add ELK_DIR and ELK_USER env var to the .profile file, which is a script that is executed when the user logs into the terminal.
# Env variables will be available every time the user opnes a terminal session 
echo "export ELK_DIR=$ELK_DIR" >> ~/.profile
echo "export ELK_USER=$ELK_USER" >> ~/.profile

# Go to ELK stack folder
cd $ELK_DIR

# Change permissions on filebat config
sudo chown root filebeat.yml 
sudo chmod go-w filebeat.yml