import getopt
import cmds.core.rasset as rasset

help_display="""
display -h : displays this help
display [-i ids] [-c countries] [-t type]: display some of the current data following some optionnal indications
    -t : Specifies nature, use commas to list arguments
    -c : Specifies country, use commas to list arguments, use double quotes if you need to use spaces
    -i : Specifies ids, you can use ranges (like n-m), use commas to list arguments
Example : display -c United_States
"""

def display(re_com,current_rassets):
	try:
		options,too_much = getopt.getopt(re_com[1:],"i:c:t:")
	except getopt.GetoptError:
		print(help_dsiplay)
		return 1,current_rassets
	if too_much :
		print(help_display)
		return 1,current_rassets
	options=dict(options)
	for key in options.keys():
		options[key]=options[key].split(',')
	ids=[]
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
			c.append('{:<24}'.format(elem))
	if '-t' in options:
		for elem in options['-t']:
			t.append("{:<6}".format(elem))
	
	display_rassets=[]
	for asset in current_rassets:
		if ((not '-i' in options) or asset.id in ids) and ((not '-c' in options) or asset.country in c) and ((not '-t' in options) or asset.nature in t):
			display_rassets.append(asset)
	rasset.display_rassets(display_rassets)
	return 1,current_rassets
