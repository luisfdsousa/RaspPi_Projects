#Set a static IP in 3 steps:

# 1: Start by editing the dhcpcd.conf file

sudo nano /etc/dhcpcd.conf

# 2: Edit / add the following lines at the bottom of the file
#    Note to specify the interface

	#interface eth0

	#static ip_address=192.168.0.10/24
	#static routers=192.168.0.1
	#static domain_name_servers=192.168.0.1

	#interface wlan0

	#static ip_address=192.168.0.200/24
	#static routers=192.168.0.1
	#static domain_name_servers=192.168.0.1

#To exit the editor, press ctrl+x
#To save your changes press the letter “Y” then hit enter

# 3: Reboot and verify if the configuration was successful 
reboot
ifconfig