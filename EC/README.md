Relevant scripts: arp_poisoning.py
Required packages: scapy,multiprocessing,time,os,pexpect,sys

method of running: 'sudo python arp_poisoning en1'
replace en1 with the interface connected to the drone network

** on ctrl-c to kill the script, we exit gracefully, setting any
configurations made on the mac back to their default values AND
undoing the ARP attack so that the user doesn't feel any service
interruptions**

Description: 
Attempts to grab the mac addr and ip of the currently connected device.
Then, grabs your mac addr and the mac addr of the drone.

Using these params, we perform arp poisoning in one thread and 
sniffing in another.  Before the sniffing is run and after the
arp poisoning has begun, we enable IP forwarding on our mac and block
tcp packets related to port 5555 (video port of the drone). 

The arp poisoning code portion (arp_poison(self)) creates an arp layer
with psource from the drone and pdest to the dev connected to the
drone, and vice versa with another arp layer. We send these two packets
out every 5 seconds, continually poisoning the arps of the phone (it now
thinks that the attacker's mac addr is associated with the dev's ip) and
the arp of the drone (it now thinks that the attacker's mac addr is 
associated with the phone's ip).

The routep_drone method, called as sniff's callback function, only runs
on packets caputed going from the drone to the phone (well, their ip addrs)
on src port 5555.  These are the video packets that the drone is intending
for the phone to receive so that it can be displayed.  With each packet,
(since the drone will have my laptop's mac addr as the dst) we replace
the packet's ethernet src mac addr with my mac's and the destination mac 
addr with the phone's. This way, we are forwarding video packets to 
our phone.  Since we use IP forwarding from the system, we do not need
to worry about other ports as these are automatically handled (note that
we do not ever lose control link when running this).  

We discovered that while packets sent to port 5555 were present, they
added a lot more runtime to handle to the routep_drone.  This caused
many Ack Fins to be sent which caused interruptions in the video
stream. **As a whole, we found that scapy's packet handling is pretty
slow for soemthing like video streaming, esp when we need to process
on one packet at a time**

******Conclusion*********
Our man in the middle attack works correctly as if we do not include the
sniff call, video connection on the device is lost, but control link works
perfectly.  This implies that all packets EXCEPT the video ones are 
reaching the device.  When we utilize the sniff call, we are sending 
video packets to the device to address the 'lot of extra credit' where
we not only replace the conventional video feed, but also respond with
the controls being issued.  As mentioned in class we have no error messages
popping up. 

Attribution:
-Baseline code used to write the MITM and arp poisoning attack
http://stackoverflow.com/questions/12659553/man-in-the-middle-attack-with-scapy
-How to block ports on mac
https://www.jamf.com/jamf-nation/discussions/13278/block-specific-outgoing-port
-How to remove port blocking
http://superuser.com/questions/539644/how-to-remove-port-forwarding-rule-on-mac
-How to enable IP forwarding
https://www.openbsd.org/faq/pf/nat.html
