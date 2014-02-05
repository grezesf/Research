#!/usr/bin/python

import os
import sys

import scipy as sp
import pickle


def main():

	# path to files to be processed
	workdir = sys.argv[1]
	# list of phones
	phone_file = sys.argv[2]
	# path where to save results
	savedir = sys.argv[3]

	# create save dirs
	if not os.path.exists(savedir):
		# print "creating sub-directory"
		os.makedirs(savedir)
	if not os.path.exists(savedir + "/train/"):
		# print "creating sub-directory"
		os.makedirs(savedir + "/train/")
	if not os.path.exists(savedir + "/test/"):
		# print "creating sub-directory"
		os.makedirs(savedir + "/test/")



	phone_list = load_phone_file(phone_file)
	# print phone_list

	cpt = 0
	train_inputs = []
	train_outputs = []
	test_inputs = []
	test_outputs = []


	# walk the directories
	for (path, dirs, files) in os.walk(workdir):
		for file in files:
			# skip the SA files
			if ".mfcc" in file  and "sa" not in file:
			# if ".mfcc" in file:
				#check if corresponding .phn file exists
				if not os.path.exists(path + "/" + file[:-8] + "phn"):
					print path + "/" + file[:-8] + "phn"
					print "corresponding .phn file does not exist!"
				else:

					print "working on: " + file
					print "from path : " + path

					cpt +=  1

					# open the files
					mfcc_file = open(path + "/" + file)
					phn_file = open(path + "/" + file[:-8] + "phn")

					# extract phone times
					phone_times = []
					for phn_line in phn_file:
						phone_times.append(phn_line.split())
					# transpose for easier use
					phone_times = map(list, zip(*phone_times))

					# skip mfcc_file header
					next(mfcc_file)

					# for each line of mfcc_file
					for mfcc_line in mfcc_file:
						# print sp.array( map( float,  line.split(";")[2:]))
						# frame start time in seconds
						start_t = mfcc_line.split(";")[1]

						# add to inputs
						if "train" in path:
							train_inputs.append( map( float,  mfcc_line.split(";")[2:]) )
						else:
							test_inputs.append( map( float,  mfcc_line.split(";")[2:]) )

						# find correspond phoneme and index in the list
						phn_index = find_phn_index(start_t, phone_times, phone_list)

						# create output of right size
						tmp_output = [-1 for x in range(len(phone_list))]
						tmp_output.insert(phn_index, 1)

						# add to outputs
						if "train" in path:
							train_outputs.append(tmp_output)
						else:
							test_outputs.append(tmp_output)


					mfcc_file.close()
					phn_file.close()


	# dump inputs and outputs to be loaded later
	f  = open(savedir + "/train/" + "train_outputs.pck", 'w')
	pickle.dump(train_outputs, f)
	f.close()
	f = open(savedir + "/test/" + "test_outputs.pck", 'w')
	pickle.dump(test_outputs, f)
	f.close()
	f  = open(savedir + "/train/" + "train_inputs.pck", 'w')
	pickle.dump(train_inputs, f)
	f.close()
	f  = open(savedir + "/test/" + "test_inputs.pck", 'w')
	pickle.dump(test_inputs, f)
	f.close()

	f = open(savedir + "/train/" + "training_data.pickle", 'w')
	pickle.dump(zip(train_inputs,train_outputs), f)
	f.close()
	f = open(savedir + "/test/" + "test_data.pickle", 'w')
	pickle.dump(zip(test_inputs,test_outputs), f)
	f.close()




def load_phone_file(phonePath):
	phones_list = []
	try:
		f = open(phonePath)
		for line in f:
			phones_list.append(line.split())
		# close f
		f.close()

	except IOError:
		print "missing phone file"


	# flatten the list using nested list comprehension
	return [val for subl in phones_list for val in subl]


def find_phn_index(start_time, phone_times, phone_list):
	# given a frame start time, a list of phone times for this audio file, and a list of phones
	# returns the list of the phone corresponding to this frame in the list

	sample_rate = 16000.0 #!!!

	for i in range( len(phone_times[0])):

		# print phone_times[0][i], float(start_time)*sample_rate, phone_times[1][i]

		if float(phone_times[0][i]) <= float(start_time)*sample_rate <= float(phone_times[1][i]):
			return phone_list.index(phone_times[2][i])

	# if nothing matches, return silence
	# this happens when the start time is beyond the last frame
	# see timit doc
	return phone_list.index("h#")

# Call to main 
if __name__=='__main__':
    main()
