#Introduce
This is a monitor for checking your host access c&c or mining pool host by dns request which collected by iTAP and stored in iMAP.

The dns-blacklist are collected from open source intelligence web site against malware.

You can get the project:
		git clone https://github.com/SuibianLiujq/personal_respo

#Platform 
You can run it on Windows or Linux with Python version 2.7, and some modules are needed:
	json  logging  datetime  time  elasticsearch  ConfigParser  socket  struct  re  requests  bs4  lxml 

#Configuration
At configuration.conf,there is 5 seections.
	[function_list] This is a list of files under the get_blacklist director,which get the blacklist from each source.
	[Windows_path] & [Linux_path]  You can configure the data path and log path on different platform.
	[frequency] You can set the start time and the period time to run it.
	[Elasticsearch] You can set the iMAP server and es port,which used to get DNS data and insert alert.

#Run
Running ontime.py to start:
		python ontime.py


