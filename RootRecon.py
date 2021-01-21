import re,sys
from cmds import get,load,save,rm,display,web,add #Charges custom commands
ascii_art="""
 _____             _   _____                      
|  __ \           | | |  __ \                     
| |__) |___   ___ | |_| |__) |___  ___ ___  _ __  
|  _  // _ \ / _ \| __|  _  // _ \/ __/ _ \| '_ \ 
| | \ \ (_) | (_) | |_| | \ \  __/ (_| (_) | | | |
|_|  \_\___/ \___/ \__|_|  \_\___|\___\___/|_| |_|
"""

quick_help="""
Commands in RootRecon console : get, load, save, display, web, rm, exit
Commands available in command line : get, add
To see more about an individual command, type : <command> -h
"""

current_rassets=[]
cookie_bgpNet_session=None
cookie_bgpNet_c=None

def toCommand(command):
	command=command.lstrip()
	start=0
	end=0
	n=len(command)
	quote=-1
	re_com=[]
	
	while end < n:
		if command[end]==' ' and quote==-1:
			if start!=end:
				re_com.append(command[start:end])
			start=end+1
		elif command[end]=='\"' and quote == -1:
			quote=end
		elif command[end]=='\"' and quote!=-1:
			if start==quote and quote+1==end :
				print("Unexpected \"\" element")
				return []
			re_com.append(command[start:quote]+command[quote+1:end])
			start=end+1
			quote=-1
		end+=1
	if start != n:
		re_com.append(command[start:])
	if quote!=-1:
		print("Pay attention to your quotes")
		return []
	return re_com

def menu():
	global current_rassets,cookie_bgpNet_session,cookie_bgpNet_c
	print('>>>',end='')
	command=input()
	re_com=toCommand(command)
	if len(re_com)>0:
		
		######  GET  ######
		if re_com[0]=='get':
			code,current_rassets,cookie_bgpNet_session,cookie_bgpNet_c=get.get(re_com,current_rassets,cookie_bgpNet_session,cookie_bgpNet_c)
		
		######  EXIT  ######
		elif re_com[0]=='exit' or re_com[0]=='bye' or re_com[0]=='stop' or re_com[0]=='quit':
			if len(re_com)>1:
				print('Enter exit to quit')
				return 1
			print('Stopping...')
			return 0
			
		######  LOAD  ######
		elif re_com[0]=='load':
			code,current_rassets=load.load(re_com,current_rassets)
		
		#### DISPLAY ####
		elif re_com[0]=='display':
			code,current_rassets=display.display(re_com,current_rassets)
			
		######  SAVE  ######
		elif re_com[0]=='save':
			code,current_rassets=save.save(re_com,current_rassets)
		
		#### REMOVE ####
		elif re_com[0]=='rm':
			code,current_rassets=rm.rm(re_com,current_rassets)
		
		### WEB ###
		elif re_com[0]=='web':
			code,current_rassets=web.web(re_com,current_rassets)
		
		### ADD ###
		elif re_com[0]=='add':
			code,current_rassets,cookie_bgpNet_session,cookie_bgpNet_c=add.add(re_com,current_rassets,cookie_bgpNet_session,cookie_bgpNet_c)
		
		#### WRONG COMMAND ####
		else:
			print(quick_help)
			return 1
		return code
	else:
		print(quick_help)
		return 1
			


if __name__=='__main__':
	if len(sys.argv)<2:
		print('Starting...')
		print(ascii_art)
		while menu():
			continue
	else:
		re_com=sys.argv[1:]
		if re_com[0]=='get':
			get.get(re_com,current_rassets,cookie_bgpNet_session,cookie_bgpNet_c)
		elif re_com[0]=='add':
			add.add(re_com,current_rassets,cookie_bgpNet_session,cookie_bgpNet_c)
		else:
			print(quick_help)
		
