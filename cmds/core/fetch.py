import requests,hashlib,re,urllib.parse,html
import cmds.core.rasset as rasset,cmds.core.convert as convert

def getFromBgpNet(search,c=None,bgp_session=None):
	"""
	Searches BGP Info on site bgp.he.net
	
	This site requires cookies, which are passed in parameters
	
	Returns the fetched info as a rasset list
	"""
	print('Getting info from bgp.he.net with search parameter : {}'.format(search))
	host="https://bgp.he.net"
	headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"}
	
	#Retrieves cookies from bgp.he.net
	if c is None:
		## Building the c and _bgp_session cookies
		#Searches the path cookie
		r1=requests.get(host+"/search?search%5Bsearch%5D={}&commit=Search".format(search),headers=headers,allow_redirects=False)
		match=re.search("path=[a-zA-Z0-9-%&/=+]{2}[a-zA-Z0-9-%&/=+]*[;\s]",r1.headers['Set-Cookie'])
		start=match.start()
		end=match.end()
		path=r1.headers['Set-Cookie'][start+5:end-1]
		path=urllib.parse.unquote(path)
		cookies={'path':path}
		
		#Searches for ext IP seen by the host
		r2=requests.get(host+'/i',headers=headers,cookies=cookies)
		ip=r2.text
	
		#MD5 Hashes of path and ip address
		i=hashlib.md5(ip.encode()).hexdigest()
		p=hashlib.md5(path.encode()).hexdigest()
	
		#Request the c and _bgp_session cookies
		r3=requests.post(host+'/jc',headers=headers,cookies=cookies,data={'p':p,'i':i})
		chaine=r3.headers['Set-Cookie']
		match=re.search("c=[a-zA-Z0-9-%&/=+]{2}[a-zA-Z0-9-%&/=+]*[;\s]",chaine)
		start=match.start()
		end=match.end()
		c=chaine[start+2:end-1]
		match=re.search("_bgp_session=[a-zA-Z0-9-%&/=+]{2}[a-zA-Z0-9-%&/=+]*[;\s]",chaine)
		start=match.start()
		end=match.end()
		bgp_session=chaine[start+13:end-1]
	
	cookies={'c':c,'_bgp_session':bgp_session}
	
	##Fetches information from bgp.he.net
	#Retrieve info
	r4=requests.get(host+"/search?search%5Bsearch%5D={}&commit=Search".format(search),headers=headers,cookies=cookies)
	search=r4.text
	
	print('Received data')
	#Extract info
	lignes=re.findall("(<tr>[\s\w\W]*?</tr>)",search)
	assets=[]
	
	for line in lignes:
		asn=re.search("AS[0-9a-zA-Z]*",line)
		ip4=re.search("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}(/[0-9][0-9])?",line)
		ip6=re.search("[:0-9a-fA-F]+[:0-9a-fA-F]+/[0-9][0-9]",line)
		nature=""
		if asn :
			start=asn.start()
			end=asn.end()
			nature="{:<6}".format("ASN")
			link=host+'/'+line[start:end]
		elif ip4:
			start=ip4.start()
			end=ip4.end()
			nature="{:<6}".format("IPv4")
			link=host+'/net/'+line[start:end]
		elif ip6:
			start=ip6.start()
			end=ip6.end()
			nature="{:<6}".format("IPv6")
			link=host+'/net/'+line[start:end]
		else:
			continue
		real_name=line[start:end]
		name="{:<32}".format(real_name)
		
		pays=re.search(r"title=.[a-zA-Z\s]*\"",line)
		if not(pays is None):
			country="{:<24}".format(line[pays.start()+7:pays.end()-1])
		else:
			country="{:<24}".format("None")
		cie="{:<24}".format("None")
		d=re.search('</td>[\w\W\s]*?<td>(?P<interest>[\w\W\s]*?<)',line)
		if not(d is None):
			description="{:<42}".format(html.unescape(urllib.parse.unquote(line[d.start('interest'):d.end('interest')-1])))
		else:
			description="{:<42}".format("None")
		assets.append(rasset.Rasset(nature,name,cie,description,country,link,real_name))
	print('Successfully loaded search data')
	
	for i in range(len(assets)):
		assets[i].id=i
	return assets,c,bgp_session


def getFromBgpView(search):
	"""
	Searches BGP info from bgpview.io
	
	Returns info as a rasset list
	"""
	print('Getting info from bgpview.io with search parameter : '+search)
	
	#Retrieve information
	host='https://bgpview.io'
	r=requests.get(host+'/search/'+search)
	search=r.text
	print('Received data')
	
	#Extract info
	lignes=re.findall("(<tr>[\s\w\W]*?</tr>)",search)
	assets=[]
	
	for ligne in lignes:
		line=re.findall("<td[\s\w\W]*?</td>",ligne)
		if len(line)<5: #Title line
			continue
		asn=re.search("AS[0-9a-zA-Z]*",line[1])
		ip4=re.search("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}(/[0-9][0-9])?",line[1])
		ip6=re.search("[:0-9a-fA-F]+[:0-9a-fA-F]+/[0-9][0-9]",line[1])
		nature=""
		if asn :
			start=asn.start()
			end=asn.end()
			nature="{:<6}".format("ASN")
			link=host+'/asn/'+line[1][start+2:end]
		elif ip4:
			start=ip4.start()
			end=ip4.end()
			nature="{:<6}".format("IPv4")
			link=host+'/prefix/'+line[1][start:end]
		elif ip6:
			start=ip6.start()
			end=ip6.end()
			nature="{:<6}".format("IPv6")
			link=host+'/prefix/'+line[1][start:end]
		else:
			continue
		real_name=line[1][start:end]
		name="{:<32}".format(real_name)
		
		pays=re.search(r"title=\"[a-zA-Z\s]*\"",line[0])
		if not(pays is None):
			country="{:<24}".format(line[0][pays.start()+7:pays.end()-1])
		else:
			country="{:<24}".format("None")
		
		d=re.search('>(?P<interest>[\w\W\s]*?<)',line[3])
		if not(d is None):
			description="{:<42}".format(html.unescape(urllib.parse.unquote(line[3][d.start('interest'):d.end('interest')-1])))
		else:
			description="{:<42}".format("None")
		
		c=re.search('>(?P<interest>[\w\W\s]*?<)',line[2])
		if not(c is None):
			cie="{:<24}".format(html.unescape(urllib.parse.unquote(line[2][c.start('interest'):c.end('interest')-1])))
		else:
			cie="{:<24}".format("None")
		assets.append(rasset.Rasset(nature,name,cie,description,country,link,real_name))
	print('Successfully loaded search data')
	
	for i in range(len(assets)):
		assets[i].id=i
	return assets

def exploreASN4(ASN_name):
	"""
	Returns the ipv4 prefixes included in the AS under a list format
	"""
	ipv4s=[]
	r=requests.get("https://bgpview.io/asn/"+ASN_name[2:])
	text=r.text
	match=re.search(r"id=\"table-prefixes-v4\"[\w\W\s]*?</div>",text)
	
	if match is None:
		return []
		
	text=text[match.start():match.end()]
	lignes=re.findall("<tr>[\w\W\s]*?</tr>",text)
	
	for line in lignes[1:]: #discard the title
		match=re.search("((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/[0-9]{2}",line)
		ipv4s.append(line[match.start():match.end()])
	
	return ipv4s
	
def exploreASN6(ASN_name):
	"""
	Returns the ipv6 prefixes included in the AS under a list format
	"""
	ipv6s=[]
	r=requests.get("https://bgpview.io/asn/"+ASN_name[2:])
	text=r.text
	match=re.search(r"id=\"table-prefixes-v6\"[\w\W\s]*?</div>",text)
	
	if match is None:
		return []
		
	text=text[match.start():match.end()]
	lignes=re.findall("<tr>[\w\W\s]*?</tr>",text)
	
	for line in lignes[1:]: #discard the title
		match=re.search("(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))/[0-9]{2}",line)
		ipv6s.append(line[match.start():match.end()])
	
	return ipv6s
	
