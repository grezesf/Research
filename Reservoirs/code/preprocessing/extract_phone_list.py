#!/usr/bin/python

import os
import sys

def main():

	# path to files to be processed
	workdir = sys.argv[1]
	# path where to save results
	savedir = sys.argv[2]

	# create save dirs
	if not os.path.exists(savedir):
		# print "creating sub-directory"
		os.makedirs(savedir)

	# phone list
	phones = []

	# walk the directories
	for (path, dirs, files) in os.walk(workdir):
		for file in files:
			if ".phn" in file:

				phn_file = open(path + "/" + file)

				for phn_line in phn_file:
					# add phone to list
					phn = phn_line.split()[2]
					if phn not in phones:
						phones.append(phn)

				phn_file.close()

	# sort alphabetically
	phones.sort()
	print phones
	
	# save to file
	f = open(savedir + "TIMIT_phone_list.txt", 'w')
	for phn in phones:
		f.write("%s\n" % phn)
	f.close()

# Call to main 
if __name__=='__main__':
    main()
