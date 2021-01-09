import getopt,re,os
from .core.fetch import *
import cmds.core.rasset as rasset

help_get="""
get -h : displays this help
get [-d directory] -s search : return the recon info from search parameter, the result can be saved automatically to a directory.
"""

def get(re_com,current_rassets,cookie_bgpNet_session,cookie_bgpNet_c):
	try:
		options,too_much=getopt.getopt(re_com[1:],"s:d:")
	except getopt.GetoptError:
		print(help_get)
		return 1,current_rassets,cookie_bgpNet_session,cookie_bgpNet_c
		
	if too_much!=[]:
		print(help_get)
		return 1,current_rassets,cookie_bgpNet_session,cookie_bgpNet_c
		
	options=dict(options)
	
	if not '-s' in options:
		print(help_get)
		return 1,current_rassets,cookie_bgpNet_session,cookie_bgpNet_c
	
	if current_rassets != [] :
		print("Warning : Current data changes will be lost. Proceed ?[y/N]", end='')
		answer=input()
		if not(answer in ['y','yes','Y','Yes','YES','YEs','yES','yeS','YeS','yEs']):
			print("Aborting...")
			return 1,current_rassets,cookie_bgpNet_session,cookie_bgpNet_c
	
	try:
		save_dir=options["-d"]
		if not os.path.isdir(save_dir):
			print('Directory does not exist. Create it ?[y/N]',end='')
			answer=input()
			if not(answer in ['y','yes','Y','Yes','YES','YEs','yES','yeS','YeS','yEs']):
				print("Aborting...")
				return 1,current_rassets,cookie_bgpNet_session,cookie_bgpNet_c
			try:
				dir_split=save_dir.split('/')
				dir=""
				for j in range(len(dir_split)):
					if dir_split[j]=="":
						continue
					dir+='/'+dir_split[j]
					if os.path.isdir(dir):
						continue
					os.mkdir(dir)
			except:
				print("Please use a valid directory name")
				return 1,current_rassets,cookie_bgpNet_session,cookie_bgpNet_c
	except KeyError:
		save_dir=None
	search=options["-s"]
	try:
		assets,cookie_bgpNet_c,cookie_bgpNet_session=getFromBgpNet(search,cookie_bgpNet_c,cookie_bgpNet_session)
		current_rassets=rasset.add_rassets(assets,getFromBgpView(search))
	except:
		print("This search parameter causes a bug, pleasereport this bug.")
		print("Aborting...")
		return 1,current_rassets,cookie_bgpNet_session,cookie_bgpNet_c
	if save_dir:
		rasset.save_rassets(current_rassets,save_dir)
	rasset.display_rassets(current_rassets)
	return 1,current_rassets,cookie_bgpNet_session,cookie_bgpNet_c
