import requests, re
import cmds.core.rasset as rasset

def toRanges(rassets):
	"""
	Turns a rasset list into a list of ASNs, a list of IPv4 prefixes and a list of IPv6 prefixes
	The IPv4 list has no duplicates, and no couples of prefixes with a subnet relationship
	"""
	ip4s=[]
	ip6s=[]
	asn=[]
	headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}
	for asset in rassets:
		if asset.nature=="{:<6}".format("ASN"):
			asn.append(asset.real_name)
		elif asset.nature=="{:<6}".format("IPv4"):
			ip4s.append(asset.real_name)
		elif asset.nature=="{:<6}".format("IPv6"):
			ip6s.append(asset.real_name)
	ip4s=list(set(ip4s))
	ip6s=list(set(ip6s))
	return (ip4s,ip6s,asn)

def strTolist(ip4s):
	"""
	Converts a list of ip adresses to binary form (with tables)
	"""
	bit_ip4s=[]
	for ip_range in ip4s:
		[ip,mask]=ip_range.split("/")
		mask=int(mask)
		ip=ip.split(".")
		bit_ip=[]
		for i in range(len(ip)):
			ip[i]=int(ip[i])
			bit_int=[0]*8
			for j in range(1,9):
				bit_int[-j]=ip[i]%2
				ip[i]=ip[i]//2
			bit_ip.extend(bit_int)
		bit_ip4s.append((mask,bit_ip))
	return bit_ip4s

def listTostr(ip4s):
	"""
	Converts a list of ip adresses under binary form (with lists) to a list of ip addresses
	"""
	str_ip4s=[]
	for (mask,bit_ip) in ip4s:
		str_ip=""
		for i in range(4):
			elem=0
			for j in range(8):
				elem+=bit_ip[i*8+j]*2**(7-j)
			str_ip=str_ip+str(elem)+'.'
		str_ip=str_ip[:-1]+"/"+str(mask)
		str_ip4s.append(str_ip)
	return str_ip4s

def reduce_ip4s(ip4s): 
	"""
	Removes duplicates and subnets
	"""
	ip4s=sorted(strTolist(ip4s))
	result=[]
	for (mask,bits) in ip4s:
		cond=True
		for (ref_mask,ref_bits_ip) in result:
			and_cond=True
			for i in range(ref_mask):
				and_cond=and_cond and (ref_bits_ip[i]==bits[i])
			cond= cond and (not and_cond)
		if cond:
			result.append((mask,bits))
	return listTostr(result)

