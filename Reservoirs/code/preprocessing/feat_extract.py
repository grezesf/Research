#!/usr/bin/python
import os
import sys


def main():
	# path to corpus
	TIMITPath = sys.argv[1]
	if "TIMIT" not in TIMITPath:
		print "TIMIT not in path, exiting."
		return None
	# path to save target
	targetDir = sys.argv[3]

	# create it if it doesnt exist
	if not os.path.exists(targetDir):
		print "Creating target directory"
		os.makedirs(targetDir)

	# path to necessary files
	SMILExtractPath = sys.argv[2]
	# conf file should be in same folder
	ConfPath = "./MFCC12_E_D_A.conf"

	# walk the directories
	for (path, dirs, files) in os.walk(TIMITPath):
		for file in files:
			if ".wav" in file:
				print "working on: " + file
				print "from path : " + path

				# create copy of TIMIT directory structure
				ind = path.split("/").index("TIMIT")
				newDir = "/".join(path.split('/')[ind+1:])
				# print newDir
				if not os.path.exists(targetDir + newDir):
					print "creating sub-directory"
					os.makedirs(targetDir + "/" + newDir )

				# perform MFCC extraction on current wav file 
				# 25ms samples every 10ms (Hamming window)
				# 12 mffc feats and 1 energy, plus deltas and accel
				base = file[:-4]
				command = SMILExtractPath + " -C " + ConfPath + " -I " + path + "/" + file + " -O " + targetDir + "/" + newDir + "/" + base + ".mfcc.csv"
				os.system(command)

	# file = "/home/felix/reservoirs/datasets/TIMIT/test/dr1/faks0/sa1.wav"
	# command = SMILExtractPath + " -C " + ConfPath + " -I " + file + " -O " + targetDir + "sa1" + ".mfcc.csv"
	# os.system(command)

# Call to main 
if __name__=='__main__':
    main()
