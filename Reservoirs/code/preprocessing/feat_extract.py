#!/usr/bin/python
import os
import sys

# README
# reads the TIMIT dataset, copies the directory structure
# performs a mffc extraction on the audio files
# input:
# TIMITPath: path to the base of the dataset directory
# SMILExtractPath: path to SMILExtract executable
# ConfPath: path to the SMILExtract configuration file
# targetDir: path the the directory in which the mffcs will be saved
# no output


def main():
	# path to corpus
	TIMITPath = os.path.abspath(os.path.normpath(sys.argv[1]))
	print TIMITPath
	if "TIMIT" not in TIMITPath:
		print "TIMIT not in path, exiting."
		return None

	# path to necessary files
	SMILExtractPath = os.path.abspath(os.path.normpath(sys.argv[2]))
	print SMILExtractPath
	# conf file spath
	ConfPath = os.path.abspath(os.path.normpath(sys.argv[3]))

	# path to save target
	targetDir = os.path.abspath(os.path.normpath(sys.argv[4]))
	print targetDir
	# create it if it doesnt exist
	if not os.path.exists(targetDir):
		print "Creating target directory"
		os.makedirs(targetDir)

	# walk the directories
	for (path, dirs, files) in os.walk(TIMITPath):
		for file in files:
			if ".wav" in file:
				print "working on: " + file
				print "from path : " + path

				# create copy of TIMIT directory structure
				ind = path.split("/").index("TIMIT")
				newDir = "/".join(path.split('/')[ind+1:])
				# print targetDir + "/" + newDir
				if not os.path.exists(targetDir + "/" + newDir):
					print "creating sub-directory"
					os.makedirs(targetDir + "/" + newDir )

				# perform MFCC extraction on current wav file 
				# 25ms samples every 10ms (Hamming window)
				# 12 mffc feats and 1 energy, plus deltas and accel
				base = file[:-4]
				command = SMILExtractPath + " -C " + ConfPath + " -I " + path + "/" + file + " -O " + targetDir + "/" + newDir + "/" + base + ".mfcc.csv"
				# print command
				os.system(command)

	# test command
	# file = "/home/felix/reservoirs/datasets/TIMIT/test/dr1/faks0/sa1.wav"
	# command = SMILExtractPath + " -C " + ConfPath + " -I " + file + " -O " + targetDir + "sa1" + ".mfcc.csv"
	# os.system(command)

	# don't return anything
	return None

# Call to main 
if __name__=='__main__':
    main()
