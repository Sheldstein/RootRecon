import os
import cmds.core.convert as convert

template="""+--------------------------------------------------------------------------------------------------------------------------------------+
|{} {} {} {} {} {} """

# each attributes that is displayed has a set number of characters :
# id :5; country : 24; nature : 6; cie_name : 24; name : 32; description : 42;

class Rasset():
	"""
	Root asset, either a ASN or an IP range, etc
	"""
	
	def __init__(self,nature,name,cie_name,description,country,link,real_name):
		self.nature=nature
		self.name=name
		self.cie=cie_name
		self.description=description
		self.id=-1
		self.country=country
		self.link=link
		self.real_name=real_name
	
	def __str__(self):
		return template.format("{:<5}".format(str(self.id)),self.name, self.nature, self.cie,self.country,self.description)

def save_rassets(rassets,directory):
	"""
	rassets : list of rassets
	directory : directory to save data
	
	The file is either created or diminished so no need to pay attention to what's in it for now
	"""
	if not os.path.isfile(directory+'/.rootrecon/rassets.txt'):
		os.mkdir(directory+'/.rootrecon/')
	else:
		print('Pre-existing data detected, saving current data will remove previous data.\nDo you want to proceed ?[y/N]:',end='')
		answer=input()
		if not(answer in ['y','yes','Y','Yes','YES','YEs','yES','yeS','YeS','yEs']):
			print("Aborting...")
			return 1
	fichier=open(directory+'/.rootrecon/rassets.txt',"w")  
	for asset in rassets:
		chaine=asset.nature+asset.name+asset.cie+asset.description+asset.country+asset.link+'|||||'+asset.real_name+'\n'
		fichier.write(chaine)  #The fixed length of everything will be useful for loading
	fichier.close()
	
	### Writing ip ranges in saved directory
	ip4s,ip6s,asn=convert.toRanges(rassets)
	f=open(directory+'/ipv4.txt',"w")
	for ip in ip4s:
		f.write(ip+'\n')
	f.close()
	f=open(directory+'/ipv6.txt',"w")
	for ip in ip6s:
		f.write(ip+'\n')
	f.close()
	f=open(directory+'/asn.txt',"w")
	for ip in asn:
		f.write(ip+'\n')
	f.close()
	print('Successfully saved data')
	return 0
	
def load_rassets(directory):
	"""
	Loads a rasset list stored in \'directory\'
	"""
	rassets=[]
	if not os.path.isfile(directory+'/.rootrecon/rassets.txt'):
		print('No data found in this directory')
		return rassets
	fichier=open(directory+'/.rootrecon/rassets.txt',"r")
	lines=fichier.readlines()
	fichier.close()
	id=0
	for line in lines:
		nature=line[0:6]
		name=line[6:38]
		cie=line[38:62]
		description=line[62:104]
		country=line[104:128]
		i=line.find('|||||')
		link=line[128:i]
		real_name=line[i+5:-1]
		rassets.append(Rasset(nature,name,cie,description,country,link,real_name))
		rassets[id].id=id
		id+=1
	return rassets

def display_rassets(rassets):
	for asset in rassets:
		print(asset)

def add_rassets(rassets1, rassets2): 
	"""
	Turns two lists of rassets with correct id without duplicates in one list with correct id without duplicates
	"""
	ajout=[]
	i=len(rassets1)
	for asset2 in rassets2:
		cond=1
		for asset1 in rassets1:
			if asset1.real_name==asset2.real_name:
				cond=0
				asset1.link=asset1.link+', '+asset2.link
				if asset1.cie=="{:<24}".format("None"):
					asset1.cie=asset2.cie
				if asset1.description=="{:<42}".format("None"):
					asset1.description=asset2.description
				if asset1.country=="{:<24}".format("None"):
					asset1.country=asset2.country
				break
		if cond:
			asset2.id=i
			i+=1
			ajout.append(asset2)
	rassets1.extend(ajout)
	return rassets1
		
