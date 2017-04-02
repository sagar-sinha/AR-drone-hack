import pexpect, sys
child = pexpect.spawn('telnet 192.168.1.1')
#re-enable the mac addr if we pass in a mac addr
if len(sys.argv) == 2 and len(sys.argv[1]) == 17:
	print "Mac addr " + sys.argv[1] + " is now being accepted by the drone"
	child.sendline('iptables -I INPUT -m mac --mac-source ' + sys.argv[1] + ' -j ACCEPT')
	child.expect(['1', ' '])
	sys.exit(0)
#Attempt to extract IP address from netstat call
try:
	child.sendline('netstat')
	child.expect('192\.168\.1\..:5559(.*)ESTABLISHED')
	raw_line = child.after
	ip = raw_line.split(' ')
	ip = [ i for i in ip if i != '' ]
	ip = ip[1][:11]
	print "The connected ip is " + str(ip)
except:
	print "Error on ip routine"
#Attempt to grab the mac addr of the IP addr with arp
try:
	child.sendline('arp -a')
	child.expect(ip + '\) at .{17}')
	macAddr = child.after[-17:]
	print "The connected mac is " + macAddr
except:
	print "Error on mac routine"
child.sendline('iptables -I INPUT -m mac --mac-source ' + macAddr + ' -j REJECT')

