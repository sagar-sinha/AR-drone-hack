Connect to the AR Drone WiFi network

Code requires pexpect (sudo easy_install pexpect) (pip)

How to install node-ar-drone:
npm install git://github.com/felixge/node-ar-drone.git

How to run command which kills other phones:
sudo python phone_block.py

This script will telnet onto the drone and use iptables to
block the mac address of the device currently connected to
the drone's ports.  This effectively kicks off the original controller.
The mac address of the kicked off device is specified so you can reenable
the device's mac addr later on.

How to re-enable phone connection:
sudo python phone_block.py [MAC ADDRESS HERE]

How to run once you are the main user:
sudo node test_fly.js

Upon keystrokes specified, make calls to node package which allow us to issue commands as if we were the phone.
See the file for keystrokes to issue commands.
___________________
Outside Resources

Stackoverflow for keystroke reading example
http://stackoverflow.com/questions/5006821/nodejs-how-to-read-keystrokes-from-stdin

How to get mac addresses (ie arp -a)
http://security.stackexchange.com/questions/64281/how-to-get-mac-address-via-ip

Example of how to do mac filtering
http://tecadmin.net/mac-address-filtering-using-iptables/#

Github used for controls
https://github.com/felixge/node-ar-drone

Used portions of example code in the git repo:
	node_modules/ar-drone/examples/simple_flight.js

