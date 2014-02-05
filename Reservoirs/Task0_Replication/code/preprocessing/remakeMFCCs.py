#!/usr/bin/python
import os
import sys

# README
# this script takes as input un-scaled MFCC files and rescales them given factors


def main():

	# path to MFCCs
	MFCCPath =  os.path.abspath(os.path.normpath(sys.argv[1]))
	# path to rescaling factors
	factorsCSV =  os.path.abspath(os.path.normpath(sys.argv[2]))
	# path to averages
	averagesCSV =   os.path.abspath(os.path.normpath(sys.argv[3]))
	# path to save results
	targetDir =  os.path.abspath(os.path.normpath(sys.argv[4]))

	# extract factors
	factors_file = open(factorsCSV)
	lines = factors_file.readlines()
	# last elem is EoL or EoF
	alphas = map( float , lines[1].split(';')[:-1])
	betas =  map( float , lines[2].split(';')[:-1])
	factors_file.close()
	# print alphas, betas

	averages_file = open(averagesCSV)
	lines = averages_file.readlines()
	averages = map( float , lines[1].split(';')[:-1])
	averages_file.close()
	# print averages


	# walk the directories
	for (path, dirs, files) in os.walk(MFCCPath):
		for file in files:
			# skip the SA files
			if ".mfcc" in file  and "sa" not in file:

				print "working on: " + file
				print "from path : " + path

				# create copy of MFCC directory structure
				ind = path.split("/").index(os.path.basename(MFCCPath))
				newDir = "/".join(path.split('/')[ind+1:])
				# print newDir
				if not os.path.exists(targetDir + "/" + newDir ):
					# print "creating sub-directory"
					os.makedirs(targetDir + "/" + newDir )

				# open mfcc file
				mfcc = open(path + "/" + file)	

				# open new file in newDir
				f = open(targetDir + "/" + newDir + "/" + file, 'w')

				# parse the mfcc file
				linecpt = 0
				for line in mfcc:
					# first line is header
					if linecpt==0:
						f.write(line)
					else:
						values = map( float , line.split(';'))
						# rescaling
						values[2:13] = [alphas[3]*betas[3]*(x-averages[3]) for x in values[2:13]]
						values[14] = alphas[0]*betas[0]*(values[14]-averages[0])
						values[15:26] = [alphas[4]*betas[4]*(x-averages[4]) for x in values[15:26]]
						values[27] = alphas[1]*betas[1]*(values[27]-averages[1])
						values[28:39] = [alphas[5]*betas[5]*(x-averages[5]) for x in values[28:39]]
						values[40] = alphas[2]*betas[2]*(values[40]-averages[2])
					
						# add line to new file
						for v in values[:-1]:
							f.write("%s;" % v)
						# add last line
						f.write("%s\n" % values[-1])


					linecpt +=1

				mfcc.close()
				f.close()





# Call to main 
if __name__=='__main__':
    main()
