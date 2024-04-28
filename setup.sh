#!/bin/bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip -y
sudo apt install libatlas-base-dev -y
sudo apt install python3-google-api-python-client -y 
sudo apt install python3-gtfs-realtime-bindings -y 
sudo apt install python3-protobuf -y 
sudo apt install python3-pandas -y
sudo apt install python3-protobuf -y
sudo apt install python3-requests -y
sudo apt install python3-flask -y
sudo apt install python3-flask-cors -y
pip install --upgrade google-api-python-client
pip install --upgrade gtfs-realtime-bindings
sudo apt install npm -y
chmod +x backend/pi_local_api.py
echo -e "//edited from initial setup\nexport const apiEndpoint = '$HOSTNAME.local'" > frontend/src/configs/apiConfig.js 
cd
sudo apt-get install -y git python3-dev python3-pillow
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix
make build-python PYTHON=$(which python3)
sudo make install-python PYTHON=$(which python3)
cd bindings/python/samples
sudo python3 runtext.py --led-cols=64 --led-gpio-mapping=adafruit-hat --text="Setup Complete!"
