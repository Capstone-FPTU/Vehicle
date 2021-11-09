sudo apt-get update && sudo apt-get upgrade
sudo pip3 install opencv-python==4.5.1.48
sudo apt-get install libhdf5-dev -y 
sudo apt-get install libhdf5-serial-dev -y 
sudo apt-get install libatlas-base-dev -y 
sudo apt-get install libjasper-dev -y 
sudo apt-get install libqtgui4 -y 
sudo apt-get install libqt4-test -y 
sudo pip3 install numpy
sudo pip3 install pytesseract
sudo pip3 install dlib imutils
sudo apt-get install python3-scipy
sudo pip3 install paho-mqtt
sudo pip3 install getmac
sudo apt install tesseract-ocr
sudo apt-get install xterm -y

sudo nano /etc/xdg/lxsession/lxde-pi/autostart
/usr/bin/chromium-browser --kiosk  --disable-restore-session-state https://sc-mavr-car.herokuapp.com/VH001


mkdir /home/pi/.config/autostart
nano /home/pi/.config/autostart/start.desktop


[Desktop Entry]
Type=Application
Name=Start
Exec=xterm -hold -e '/usr/bin/python3 /home/pi/Desktop/Vehicle/start.py'
