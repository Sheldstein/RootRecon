import getopt,re,os
from .core.fetch import *
import cmds.core.rasset as rasset

help_add="""
add -h : displays this help
add -s search [-o output]: add the result of a search to the data stored in the -o directory
add -d directory [-o output]: add the result stored in the -d directory to the data stored in the -o directory

If the -o option is not set, add to current data. You should always set the -o option in command line

RootRecon console only :
add -o directory : add current data to the data saved in the ouput directory
"""

def add(re_com,current_rassets,cookie_bgpNet_c,cookie_bgpNet_session):
	save_dir=None
	search=None
	load_dir=None
	
	try:
		options,too_much=getopt.getopt(re_com[1:],"d:o:s:")
		options=dict(options)
	except getopt.GetoptError:
		print(help_add)
		return 1,current_rassets,cookie_bgpNet_c,cookie_bgpNet_session
	if too_much:	
		print(help_add)
		return 1,current_rassets,cookie_bgpNet_c,cookie_bgpNet_session
	
	if '-d' in options:
		load_dir=options['-d']
		if not os.path.isdir(load_dir):
			print("Please use an existing directory after -d option")
			return 1,current_rassets,cookie_bgpNet_c,cookie_bgpNet_session
	if '-o' in options:
		save_dir=options['-o']
		if not os.path.isdir(save_dir):
			print("Please use an existing directory after -d option")
			return 1,current_rassets,cookie_bgpNet_c,cookie_bgpNet_session
	if '-s' in options:
		search=options['-s']
	
	if (load_dir is None and search is None and save_dir is None) or (load_dir and save_dir):
		print(help_add)
		return 1,current_rassets,cookie_bgpNet_c,cookie_bgpNet_session
	if search:
		assets,cookie_bgpNet_c,cookie_bgpNet_session=getFromBgpNet(search,cookie_bgpNet_c,cookie_bgpNet_session)
		added_rassets=rasset.add_rassets(assets,getFromBgpView(search))
		current_rassets=rasset.add_rassets(current_rassets,added_rassets)
	elif load_dir:
		added_rassets=rasset.load_rassets(load_dir)
		if added_rassets==[]:
			print("Please enter a directory with data after the -d option")
			return 1,current_rassets,cookie_bgpNet_c,cookie_bgpNet_session
		if save_dir:
			saved_rassets=rasset.load_rassets(save_dir)
			if saved_rassets==[]:
				print("Please enter a directory with data after the -o option")
				return 1,current_rassets,cookie_bgpNet_c,cookie_bgpNet_session
			print("Warning : Current data changes will be lost. Proceed ?[y/N]", end='')
			answer=input()
			if not(answer in ['y','yes','Y','Yes','YES','YEs','yES','yeS','YeS','yEs']):
				print("Aborting...")
				return 1,current_rassets,cookie_bgpNet_c,cookie_bgpNet_session
			current_rassets=rasset.add_rassets(saved_rassets,added_rassets)
		else:
			current_rassets=rasset.add_rassets(current_rassets,added_rassets)
	elif save_dir:
		tmp=current_rassets
		saved_rassets=rasset.load_rassets(save_dir)
		current_rassets=rasset.add_rassets(saved_rassets,current_rassets)
		rasset.save_rassets(save_dir)
		print("Successfully added data")
		current_rassets=tmp
		return 1,current_rassets,cookie_bgpNet_c,cookie_bgpNet_session
			
	if save_dir:
		rasset.save_rassets(current_rassets,save_dir)
	rasset.display_rassets(current_rassets)
	return 1,current_rassets,cookie_bgpNet_c,cookie_bgpNet_session
