# Introduce
This is a monitor for checking your host access c&c or mining pool host by dns request which collected by iTAP and stored in iMAP.
<br>
The dns-blacklist are collected from open source intelligence web site against malware.
<br>
You can get the project:
<br>		git clone https://github.com/SuibianLiujq/personal_respo
<br>
# Platform 
You can run it on Windows or Linux with Python version 2.7, and some modules are needed:
<br>	json  logging  datetime  time  elasticsearch  ConfigParser  socket  struct  re  requests  bs4  lxml 
<br>
# Configuration
At configuration.conf,there is 5 seections.
<br>	[function_list] This is a list of files under the get_blacklist director,which get the blacklist from each source.
<br>	[Windows_path] & [Linux_path]  You can configure the data path and log path on different platform.
<br>	[frequency] You can set the start time and the period time to run it.
<br>	[Elasticsearch] You can set the iMAP server and es port,which used to get DNS data and insert alert.

# Run
Running ontime.py to start:
<br>		python ontime.py


