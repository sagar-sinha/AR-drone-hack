## Import Scapy module
import time
from scapy.all import *
import subprocess

stream_started = False
current_ts = -1
frame = ""
last_seq = set()

def add_frame(frame):
    global stream_started
    if frame[:4] != 'PaVE':
        return
    video = open('stream.h264', 'a')
    for letter in frame:
        video.write(letter)
    video.close()
    if stream_started is False:
        p = subprocess.Popen("ffplay -i stream.h264".split())
        stream_started = True
    return


## Define our Custom Action function
def customAction(packet):
	global current_ts
	global frame
	global last_seq
	if IP in packet:
		ip_src=packet[IP].src
	else:
		print "no ip"
		return
	if TCP in packet:
		tcp_sport=packet[TCP].sport
		if ip_src != '192.168.1.1':
			print "bad ip source: " + str(ip_src)
			return
		if tcp_sport != 5555:
			print "bad port source"
			return
		try:
			seq= packet[TCP].seq
			if seq in last_seq:
				return
			else:
				if len(last_seq) > 1000:
					print "resetting size"
					last_seq = set()
				last_seq.add(seq)
			ts= packet[TCP].options[2][1][0]            
			payload = packet[Raw].load
			if current_ts == -1:
				current_ts = ts
			elif current_ts != ts:
				add_frame(frame)
				frame = ""
				current_ts = ts
			frame += payload
		except:
			return



## Setup sniff, filtering for IP traffic
subprocess.Popen(['sudo', 'rm', 'stream.h264'])
subprocess.Popen(['sudo', 'rm', 'captured.pcap'])
subprocess.check_output(['sudo', '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '--channel=6'])
#proc = subprocess.Popen(['sudo', 'tcpdump', '-I', '-P', '-i', 'en0', 'src', '192.168.1.1', 'and', 'port', '5555', '-w', 'captured.pcap']);
try: 
	while True:
		subprocess.Popen(['sudo', 'rm', 'temp.pcap'])
		proc = subprocess.Popen(['sudo', 'tcpdump', '-I', '-P', '-i', 'en0', 'src', '192.168.1.1', 'and', 'port', '5555', '-w', 'temp.pcap'], shell=False);    	
		try:	
			x = sniff(offline='temp.pcap', prn = customAction, timeout=1, store=0)
		except Scapy_Exception as e:
			print "Bad sniff on error: " + str(e)
		finally:
			time.sleep(1)
			subprocess.Popen(['sudo', 'kill', '-2', str(proc.pid)])
except KeyboardInterrupt:
	subprocess.Popen(['sudo', 'pkill', 'tcpdump'])
	subprocess.Popen(['sudo', 'rm', 'temp.pcap'])
	print("User Ended Video Feed")  
