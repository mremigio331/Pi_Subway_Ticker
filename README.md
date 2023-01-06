# Pi Subway Ticker
![Output](Images/Penn_station.jpg)
Pi Subway Ticker connects to the NYC API and displays live arrival data using a Raspbery Pi and a LED matrix. It is currently usable only for a 64x32 LED matrix using an adafruit hat. 

## To install all dependencies needed:

$ pip install -r requirements.txt

## To run the code input the following:

$ python3 pi_subway_ticker.py

## MTA API Keys

You will need to create an account with the MTA in order to pull live data. To do so visit the following page https://new.mta.info/developers. 

![Output](Images/Yankee_stadium.jpg)

## Future Plans
* Create a website that is hosted locally to change the station and see all MTA info
* More robust errors to better identify what when wrong
* Support for LIRR and Metro North