#Start by editing the dhcpcd.conf file

sudo nano /etc/dhcpcd.conf

# Edit / add the following lines at the bottom of the file
# Note to specify the interface

	#interface eth0

	#static ip_address=192.168.0.10/24
	#static routers=192.168.0.1
	#static domain_name_servers=192.168.0.1

	#interface wlan0

	#static ip_address=192.168.0.200/24
	#static routers=192.168.0.1
	#static domain_name_servers=192.168.0.1
