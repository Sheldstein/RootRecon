import getopt,os
import cmds.core.rasset as rasset

help_save="""
save -h : displays this help
save -d directory : save data to this directory
"""

def save(re_com,current_rassets):
	try:
		options,too_much=getopt.getopt(re_com[1:],"d:")
	except getopt.GetoptError:
		print(help_save)
		return 1,current_rassets
	if too_much:
		print(help_save)
		return 1,current_rassets
	options=dict(options)
	try:
		save_dir=options["-d"]
		if not os.path.isdir(save_dir):
			print('Directory does not exist. Create it ?[y/N]',end='')
			answer=input()
			if not(answer in ['y','yes','Y','Yes','YES','YEs','yES','yeS','YeS','yEs']):
				print("Aborting...")
				return 1,current_rassets
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
				return 1,current_rassets
	except KeyError:
		print(help_save)
		return 1,current_rassets
			
	if current_rassets==[]:
		print('Nothing to save')
		return 1,current_rassets
	rasset.save_rassets(current_rassets,save_dir)
	return 1,current_rassets
