import getopt
import cmds.core.rasset as rasset

help_rm="""
rm -h : displays this help
rm [-i ids] [-c countries] [-n countries] [-t type]: removes assets from current data. Editions are not automatically saved
	-i : Followed by a comma-separated list of ids/ranges (like n-m)
	-c : Followed by a comma-separated list of countries that you remove ( if there is a space in a country, use a '_' )
	-n : Followed by a space-separated list of countries that you keep ( if there is a space in a country, use a '_' )
	-t : Followed by a comma-separated list of types of assets that you remove (ASN, IPv4, etc)
"""

def rm(re_com,current_rassets):
	try:
		options,too_much = getopt.getopt(re_com[1:],"i:c:n:t:")
	except getopt.GetoptError:
		print(help_rm)
		return 1,current_rassets
	if too_much :
		print(help_rm)
		return 1,current_rassets
	options=dict(options)
	for key in options.keys():
		options[key]=options[key].split(',')
	ids=[]
	nc=[]
	c=[]
	t=[]
	if '-i' in options:
		for elem in options['-i']:
			try:
				index=elem.find('-')
				if index==-1:
					ids.append(int(elem))
				else:
					ids.extend([j for j in range(int(elem[:index]),int(elem[index+1:])+1)])
			except:
				print("Please enter valid ids")
				return 1,current_rassets
	if '-c' in options:
		for elem in options['-c']:
			c.append('{:<24}'.format(elem).replace("_"," "))
	if '-n' in options:
		for elem in options['-n']:
			nc.append('{:<24}'.format(elem).replace("_"," "))
	if '-t' in options:
		for elem in options['-t']:
			t.append("{:<6}".format(elem))
	
	if options=={}:
		print(help_rm)
		return 1,current_rassets
	
	keep_rassets=[]
	for asset in current_rassets:
		if (not asset.id in ids) and (not asset.country in c) and ((not '-n' in options) or asset.country in nc) and (not asset.nature in t):
			keep_rassets.append(asset)
	current_rassets=keep_rassets
	for i in range(len(current_rassets)):
		current_rassets[i].id=i
	rasset.display_rassets(current_rassets)
	return 1,current_rassets
