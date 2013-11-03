#!/usr/bin/python
import os
import sys
import math


def main():

	# path to MFCCs
	MFCCPath = sys.argv[1]
	# path to save results
	targetDir = sys.argv[2]

	# create it if it doesnt exist
	if not os.path.exists(targetDir):
		print "Creating target directory"
		os.makedirs(targetDir)

	# useful variables
	nbFiles = 0
	nbFrames = 0

	# values to calculate
	averages = [0,0,0,0,0,0]
	alphas = [0,0,0,0,0,0]

	# # Counting
	# # walk the directories
	# for (path, dirs, files) in os.walk(MFCCPath):
	# 	for file in files:
	# 		# look only at train files (of mfccs of course)
	# 		# if ".mfcc" in file and "/train/" in path:
	# 		if ".mfcc" in file and "sa" not in file:

	# 			# print "working on: " + file
	# 			# print "from path : " + path

	# 			nbFiles+=1

	# print nbFiles




	# walk the directories
	for (path, dirs, files) in os.walk(MFCCPath):
		for file in files:
			# look only at train files (of mfccs of course)
			# skip the SA files
			if ".mfcc" in file  and "sa" not in file and "/train/" in path:
			# if ".mfcc" in file  and "sa" not in file:

				# print "working on: " + file
				# print "from path : " + path

				nbFiles+=1
				
				f = open(path + "/" + file)
				# skip first line (header)
				next(f)
				for line in f:

					nbFrames+=1

					averages[0] += float( line.split(";")[14] )
					averages[1] += float( line.split(";")[27] )
					averages[2] += float( line.split(";")[40] )
					averages[3] += sum( map( float , line.split(";")[2:13] ))
					averages[4] += sum( map( float , line.split(";")[15:26] ))
					averages[5] += sum( map( float , line.split(";")[28:39] ))


				f.close()

	# compute averages
	averages = [x/nbFrames for x in averages]
	averages[3:] = [x/12 for x in averages[3:]]


	# 2nd pass through data
	# walk the directories
	for (path, dirs, files) in os.walk(MFCCPath):
		for file in files:      
			# # look only at train files (of mfccs of course)
			if ".mfcc" in file  and "sa" not in file and "/train/" in path:
			# if ".mfcc" in file  and "sa" not in file:

				# print "working on: " + file
				# print "from path : " + path

				f = open(path + "/" + file)
				# skip first line (header)
				next(f)
				for line in f:

					# l1 norm
					alphas[0] += abs(float( line.split(";")[14] ) - averages[0])
					alphas[1] += abs(float( line.split(";")[27] ) - averages[1])
					alphas[2] += abs(float( line.split(";")[40] ) - averages[2])
					alphas[3] += sum( [ abs(x-averages[3]) for x in  map( float , line.split(";")[2:13] )] ) 
					alphas[4] += sum( [ abs(x-averages[4]) for x in  map( float , line.split(";")[15:26] )] ) 
					alphas[5] += sum( [ abs(x-averages[5]) for x in  map( float , line.split(";")[28:39] )] ) 

					# inf norm
					# alphas[0] = max( abs(float( line.split(";")[14] ) - averages[0]) , alphas[0])
					# alphas[1] = max( abs(float( line.split(";")[27] ) - averages[1]) , alphas[1])
					# alphas[2] = max( abs(float( line.split(";")[40] ) - averages[2]) , alphas[2])


				f.close()

	# average out
	print "nbFiles = " , nbFiles
	print "nbFrames =" , nbFrames
	print "averages = " , averages
	print "sum = ", alphas
	alphas = [nbFrames/x for x in alphas]
	alphas[3:] = [12*x for x in alphas[3:]]
	print "alphas = " , alphas


	# save results to files
	f = open(targetDir + "averages.csv", 'w')
	f.write( "log(E);de_log(E);dede_log(E);cepstrum;de_cepstrum;dede_cepstrum\n")
	for a in averages:
	  f.write("%s;" % a)
	f.close()

	f = open(targetDir + "alphas.csv", 'w')
	f.write( "log(E);de_log(E);dede_log(E);cepstrum;de_cepstrum;dede_cepstrum\n")
	for a in alphas:
	  f.write("%s;" % a)
	f.close()

# Call to main 
if __name__=='__main__':
    main()
