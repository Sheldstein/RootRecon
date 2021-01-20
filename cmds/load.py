import getopt,os
import cmds.core.rasset as rasset

help_load="""
load -h : displays this help
load -d directory : loads data from this directory
"""

def load(re_com,current_rassets):
	try:
		options,too_much=getopt.getopt(re_com[1:],"d:")
	except getopt.GetoptError:
		print(help_load)
		return 1,current_rassets
		
	if too_much!=[]:
		print(help_load)
		return 1,current_rassets
		
	options=dict(options)
	
	try:
		dir=options['-d']
	except KeyError:
		print(help_load)
		return 1,current_rassets
	if not os.path.isdir(dir):
		print("Please enter an existing directory")
		return 1,current_rassets
	if current_rassets!=[]:
		print("Current data will be discarded. Continue ?[y/N]",end='')
		answer=input()
		if not(answer in ['y','yes','Y','Yes','YES','YEs','yES','yeS','YeS','yEs']):
			print("Aborting...")
			return 1,current_rassets
	current_rassets=rasset.load_rassets(dir)
	rasset.display_rassets(current_rassets)
	return 1,current_rassets
