#!/bin/bash

# Get the current user
USER=$(whoami)

# Update and upgrade system packages
install_system_packages() {
    echo "Updating and upgrading system packages..."
    sudo apt update && sudo apt upgrade -y
    # Pre-seed answers for iptables-persistent installation
    echo iptables-persistent iptables-persistent/autosave_v4 boolean true | sudo debconf-set-selections
    echo iptables-persistent iptables-persistent/autosave_v6 boolean true | sudo debconf-set-selections
    # Install required packages
    sudo apt install -y python3-pip libatlas-base-dev python3-protobuf python3-pandas python3-requests python3-flask python3-flask-cors avahi-daemon git python3-dev python3-pillow iptables-persistent
    sudo apt install -y python3-flasgger python3-pip python3-botocore python3-boto3 screen default-jdk wget curl unzip
    sudo pip3 install fastapi uvicorn black watchdog --break-system-packages
    echo "System packages installed."
}

# Check and install or upgrade Node.js to version 18.x
install_node() {
    echo "Checking for Node.js installation..."
    if command -v node &>/dev/null; then
        NODE_VERSION=$(node -v)
        if [[ "$NODE_VERSION" == "v18."* ]]; then
            echo "Node.js version 18 is already installed."
            return
        else
            echo "Node.js is installed but not version 18, upgrading..."
        fi
    else
        echo "Node.js is not installed. Installing..."
    fi
    sudo apt remove -y nodejs npm
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt install -y nodejs
    echo "Node.js version 18 has been installed."
}

# Install Python packages
install_python_packages() {
    echo "Installing Python packages..."
    python3 -m pip install --upgrade pip --break-system-packages
    python3 -m pip install google-api-python-client gtfs-realtime-bindings Cython --break-system-packages
    echo "Python packages installed."
}

# Clone and setup external projects like rpi-rgb-led-matrix
setup_external_projects() {
    echo "Setting up external projects..."
    if [ ! -d "/home/$USER/rpi-rgb-led-matrix" ]; then
        git clone https://github.com/hzeller/rpi-rgb-led-matrix.git /home/$USER/rpi-rgb-led-matrix
        cd /home/$USER/rpi-rgb-led-matrix
        
        export PATH=$PATH:~/.local/bin
        
        # Build and install
        if ! make build-python PYTHON=$(which python3); then
            echo "Error: Failed to build. Ensure cython is installed and in the PATH."
            exit 1
        fi
        
        if ! sudo make install-python PYTHON=$(which python3); then
            echo "Error: Failed to install. Ensure cython is installed and in the PATH."
            exit 1
        fi
        
        echo "rpi-rgb-led-matrix set up."
    else
        echo "rpi-rgb-led-matrix already installed."
    fi
    cp -r /home/$USER/rpi-rgb-led-matrix/bindings/python/rgbmatrix/ /home/$USER/Pi_Subway_Ticker/backend/
}

# Setup port forwarding
setup_port_forwarding() {
    echo "Setting up port forwarding..."
    if ! sudo iptables -t nat -C PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080 2>/dev/null; then
        sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
        sudo netfilter-persistent save
        echo "Port forwarding rule established."
    else
        echo "Port forwarding rule already exists."
    fi
}

# Install frontend npm packages
install_frontend_packages() {
    echo "Installing frontend npm packages..."
    cd /home/$USER/Pi_Subway_Ticker/frontend
    npm install
    printf "//edited from initial setup\nexport const apiEndpoint = '$HOSTNAME.local'\n" > /home/$USER/Pi_Subway_Ticker/frontend/src/configs/apiConfig.js
    echo "Frontend npm packages installed."
}

# Set executable permissions
set_executable_permissions() {
    echo "Setting executable permissions..."
    chmod +x /home/$USER/Pi_Subway_Ticker/backend/pi_local_api.py
    chmod +x /home/$USER/Pi_Subway_Ticker/subway_start.sh
    echo "Executable permissions set."
}

# Add cron job if it does not already exist
add_cron_job() {
    echo "Adding cron job..."
    local job_command="@reboot sleep 30 && cd /home/$USER/Pi_Subway_Ticker && ./subway_start.sh >> /home/$USER/Pi_Subway_Ticker/subway_start.log 2>&1"

    if ! (sudo crontab -l 2>/dev/null | grep -Fq -- "$job_command"); then
        ( crontab -l 2>/dev/null; echo "$job_command") | crontab -
        echo "Cron job added."
    else
        echo "Cron job already exists."
    fi
}

# Controlled reboot with a 30-second countdown and an option to cancel
reboot_system() {
    echo "Preparing to reboot the system to ensure all configurations are applied..."
    echo "Press Enter to reboot now or Ctrl+C to cancel."
    
    # Wait for the user to press Enter
    read -p "Press Enter to continue..." -r
    
    # If user presses Enter, the script proceeds to reboot
    echo "Rebooting now..."
    sudo reboot
}

# Change ownership of the project directory to the current user
change_ownership() {
    echo "Changing ownership of the project directory to the current user..."
    sudo chown -R $USER:$USER /home/$USER/Pi_Subway_Ticker
    echo "Ownership changed."
}

# Create log directory and set permissions
create_log_directory() {
    local log_dir=$1
    echo "Creating log directory at $log_dir..."
    sudo mkdir -p $log_dir
    echo "Setting permissions for user $USER..."
    sudo chown $USER:$USER $log_dir
    sudo chmod 750 $log_dir
}

# Create logrotate configuration
create_logrotate_config() {
    local log_file=$1
    local logrotate_config="/etc/logrotate.d/$(basename $log_file)"
    echo "Creating logrotate configuration for $log_file at $logrotate_config..."
    sudo bash -c "cat > $logrotate_config" <<EOL
$log_file {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 640 $USER $USER
}
EOL
}

# Setup log files
setup_log_files() {
    LOG_DIR="/var/log/subway_ticker"
    create_log_directory "$LOG_DIR"
    create_logrotate_config "$LOG_DIR/website.log"
    create_logrotate_config "$LOG_DIR/api.log"
    create_logrotate_config "$LOG_DIR/device.log"
}

# Execute all setup functions in the optimal order
install_system_packages
install_node
install_python_packages
setup_external_projects
setup_port_forwarding
change_ownership
install_frontend_packages
set_executable_permissions
setup_log_files
# add_cron_job
# reboot_system