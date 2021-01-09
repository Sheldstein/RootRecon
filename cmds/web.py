import getopt,webbrowser
import cmds.core.rasset as rasset

help_web="""
web -h : displays this help
web -i ids : opens the information pages found for specified assets in the default web browser. Supports ranges, lists of parameters (separated by commas)
"""

def web(re_com,current_rassets):
	try:
		options,too_much=getopt.getopt(re_com[1:],"i:")
	except getopt.GetoptError:
		print(help_web)
		return 1,current_rassets
	if too_much:
		print(help_web)
		return 1,current_rassets
	options=dict(options)
	try:
		ids=[]
		options['-i']=options['-i'].split(',')
		for elem in options['-i']:
			try:
				index=elem.find('-')
				if index==-1:
					ids.append(int(elem))
				else:
					ids.extend([j for j in range(int(elem[:index]),int(elem[index+1:])+1)])
			except:
				print("Please make sure to use valid ids")
				return 1,current_rassets
		ids=sorted(list(set(ids)))
		try :
			for i in ids:
				links=current_rassets[i].link.split(', ')
				for link in links:
					try:
						webbrowser.open(link,new=2)
						print(link)
					except:
						continue
			return 1,current_rassets
		except IndexError:
			print("Only use attributed ids")
			return 1,current_rassets
	except KeyError:
		print(help_web)
		return 1,current_rassets
