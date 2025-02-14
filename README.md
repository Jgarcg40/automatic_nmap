Automatic nmap is a python script that allows you to do the most common nmap scans in a single run + whatweb. 

**Usage**: to run it you have to put python3 nmap_script.py <IP> <Scan type (sS or tcp sync scan or UDP)> 
If no scan type is specified it will do a deeper but slower scan.

**Requirements**: have installed the python libraries sys, subprocess, re and os (with pip install <library>), 
nmap and whatweb (sudo apt install nmap && sudo apt install whatweb).

