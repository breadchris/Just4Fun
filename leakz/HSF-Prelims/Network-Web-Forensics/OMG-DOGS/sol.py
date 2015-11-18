import dpkt

i = file('dat.pcap', 'rb')

o = open('out', 'w')

pcap = dpkt.pcap.Reader(i)

for ts, buf in pcap:
	eth = dpkt.ethernet.Ethernet(buf)
	if (eth.type != 2048): # 2048 is the code for IPv4
		continue

	ip=eth.data
	icmp=ip.data

	if (ip.p==dpkt.ip.IP_PROTO_ICMP) and len(icmp.data.data)>256:
		try:
			#print icmp.data.data
			o.write(icmp.data.data)
		except:
			print 'Error extracting ICMP payload data from this packet.'
			continue

i.close()
o.close()
