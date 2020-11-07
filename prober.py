#!/usr/bin/python
# Simple Service Performance implemented by python writen by Mohammad Hossein Abdsharifi

""" Make sure you have installed python3 in Linux machin.
Input format should be as follow: 
python3 prober.py <Agent IP:port:community> <sample frequency> <samples> <OID1> <OID2> …….. <OIDn> 
IP, port and community are agent details
OIDn are the OIDs to be probed 
Sample frequency  (Fs) is the sampling frequency expressed in Hz, you should handle between 10 and 0.1 Hz 
Samples (N) is the number of successful samples the solution should do before terminating """

""" importing required libraries """
import easysnmp, sys, time, math
from easysnmp import snmp_get, snmp_walk, Session

""" Defining varibles and lists and extracting data from user input"""
deviceInfo = sys.argv[1]
s = deviceInfo.split(':')
device_ip = s[0] # agent ip number
device_port = s[1] # agent port number
device_community = s[2] # community number
device_frequency = float(sys.argv[2])
instance = int(sys.argv[3])
instance_clock = (1/device_frequency) # Calculating sample time in OID
OID = [] # List for keeping OID values

""" Extract and save the number of OID's inserted by user in command line """
for items in range(4, len(sys.argv)):
    OID.append(sys.argv[items])
OID.insert(0, '1.3.6.1.2.1.2.2.1.10.2')

""" Defining empty list to keep OID values for further calculations """
old_OID = [] 
current_OID = []

##############################
def prober():
    """ Main Funtion """ 
    global current_time # making visible from outside function
    global current_OID # making visible from outside function
    
    request = Session(hostname=device_ip, remote_port=device_port,
    community='public',version=2,timeout=1,retries=1)
    reply = request.get(OID)
    old_OID = []
    
    for extract_oid in range(1, len(reply)):
        OID_math = (extract_oid - 1)
        if reply[extract_oid].value!= 'NOSUCHOBJECT' and reply[extract_oid].value!='NOSUCHINSTANCE':
            old_OID.append(int(reply[extract_oid].value))
             
            if count!=0 and len(current_OID)>0:
                
                OID_diffrential = (int(old_OID[OID_math]) - int(current_OID[OID_math])) 
                OID_time = old_time - current_time
                time_differentila = round(OID_time, 1)
                rate_math = (OID_diffrential / time_differentila)
                OID_rate = int(rate_math)

                if OID_rate < 0:
                    if reply[extract_oid].snmp_mode == 'COUNTER32':
                        OID_diffrential = (OID_diffrential) + (2^32)
                        # print out resutls in required format
                        print(f"{str(old_time)}  |  {str(rate_math)}  |") 

                    elif reply[extract_oid].snmp_mode == 'COUNTER64':
                        OID_diffrential = (OID_diffrential) + (2^64)
                        # print out resutls in required format
                        print(f"{str(old_time)}  |  {str(rate_math)}  |") 

                else:
                    # print out resutls in required format
                    print(f"{str(old_time)}  |  {str(OID_rate)}  |") 

########################################

    current_OID = old_OID
    current_time = old_time

if instance == -1:
    count = 0
    current_OID = []

    flag = True
    while flag:
        old_time = (time.time())
        prober()
        reply_time = (time.time())
        count = count + 1
        # Time for next probe
        time.sleep(abs(instance_clock - reply_time + old_time)) 

else:
    current_OID = []

    for count in range(0, instance+1):
        old_time = time.time()
        prober()
        reply_time = time.time()
        # Time for next probe
        time.sleep(abs(instance_clock - reply_time + old_time))
########################################