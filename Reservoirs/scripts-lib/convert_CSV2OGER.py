#!/usr/bin/python

import os
import sys
import numpy
import cPickle as pickle
import datetime


### README
# This script reads a directory adn sub-directory for csv files representing MFCC extractions
# it then packages those files as pickles for easy loading OGER later
# It is only meant to be run on /TIMIT-MFCCs
# it should create train_inputs.pck and test_inputs.pck (divide as TIMIT is)

# at the same time it saves the phone label of each MFCC frame into a train_target.pck and test_target.pck

# to avoid bias, the SA sentences (the same 2 for each speaker), are skipped
# these output files should be reservoir ready

def main():

	# path to files to be processed
	if not sys.argv[1:]:
		# default arguments if none provided
		# /dir in which the mffc files are
		workdir = "/home/felix/Research/Reservoirs/datasets/TIMIT-MFCCs"
		# list of phones
		phone_file = "/home/felix/Research/Reservoirs/datasets/TIMIT_phone_list.txt"
		# path where to save results
		savedir = "/home/felix/Research/Reservoirs/datasets/TIMIT-OGER"

	else:
		# /dir in which the mffc files are
		workdir = sys.argv[1]
		# list of phones
		phone_file = sys.argv[2]
		# path where to save results
		savedir = sys.argv[3]

	print "workdir:", workdir
	print "phone list file:", phone_file
	print "savedir:", savedir

	# create save dirs
	if not os.path.exists(savedir):
		print "creating sub-directory"
		os.makedirs(savedir)
	if not os.path.exists(savedir + "/train/"):
		print "creating sub-directory"
		os.makedirs(savedir + "/train/")
	if not os.path.exists(savedir + "/test/"):
		print "creating sub-directory"
		os.makedirs(savedir + "/test/")
	if not os.path.exists(savedir + "/dev/"):
		print "creating sub-directory"
		os.makedirs(savedir + "/dev/")

	# create description file
	print "creating description file"
	f = open(savedir + "/" + "description.txt", 'w')
	f.write("This directory contains OGER-ready version of the mffc extractions from the audio files of the TIMIT dataset.\n")
	f.write("The SA sentences (the same 2 for each speaker) were removed to avoid bias.\n")
	f.write("This directory was created by /script-lib/convert_CVS2OGER.py on " + str(datetime.date.today()) + "\n")
	f.close()

	phone_list = load_phone_file(phone_file)
	# print phone_list

	train_file_cnt = 0
	test_file_cnt = 0
	train_inputs = []
	train_targets = []
	test_inputs = []
	test_targets = []
	dev_inputs = []
	dev_targets = []

	# OGER files are dimensioned as follows
	# (nb_data_instances, nb_data_point_per_instance, nb_dim_per_data_point)
	# in this case it should be
	# (nb_mfcc_files, nb_frames, nb_dim_per_frame=39)


	# walk the directories
	for (path, dirs, files) in os.walk(workdir):
		for file in files:
			# skip the SA files
			if ".mfcc" in file  and "sa" not in file:
				#check if corresponding .phn file exists
				if not os.path.exists(path + "/" + file[:-8] + "phn"):
					print path + "/" + file[:-8] + "phn"
					print "corresponding .phn file does not exist!"
				else:

					# create instances
					input_instance = []
					target_instance = []

					print "working on: " + file
					print "from path : " + path

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

					# reset frame count
					frame_cnt = 0

					# for each line of mfcc_file
					for mfcc_line in mfcc_file:

						# increment frame count
						frame_cnt += 1 

						# print "frame line #:", frame_cnt 

						# frame start time in seconds
						start_t = mfcc_line.split(";")[1]

						# create frame (skiping first 2 values, frame_index and frame_time)
						frame = map( float,  mfcc_line.split(";")[2:])
						# print numpy.shape(frame)
						# print frame

						# find correspond phoneme and index in the list
						phn_index = find_phn_index(start_t, phone_times, phone_list)

						# create target of right size
						target = [-1 for x in range(len(phone_list))]
						target.insert(phn_index, 1)

						# add to instances
						input_instance.append(frame)
						target_instance.append(target)

					# once the mffc file is parsed, add to datasets
					if "train" in path:
						train_file_cnt += 1
						train_inputs.append(numpy.array(input_instance))
						train_targets.append(numpy.array(target_instance))
					else:
						test_file_cnt += 1
						test_inputs.append(numpy.array(input_instance))
						test_targets.append(numpy.array(target_instance))

					# add to dev files
					if ((train_file_cnt+test_file_cnt)%30) == 0:
						dev_inputs.append(numpy.array(input_instance))
						dev_targets.append(numpy.array(target_instance))

					mfcc_file.close()
					phn_file.close()


	print numpy.shape(train_inputs)
	print numpy.shape(train_targets)
	print numpy.shape(test_inputs)
	print numpy.shape(test_targets)
	print numpy.shape(dev_inputs)
	print numpy.shape(dev_targets)

	# dump inputs and outputs to be loaded later 
	f  = open(savedir + "/train/" + "train_targets.pck", 'w')
	pickle.dump(numpy.array(train_targets), f)
	f.close()
	f = open(savedir + "/test/" + "test_targets.pck", 'w')
	pickle.dump(numpy.array(test_targets), f)
	f.close()
	f  = open(savedir + "/train/" + "train_inputs.pck", 'w')
	pickle.dump(numpy.array(train_inputs), f)
	f.close()
	f  = open(savedir + "/test/" + "test_inputs.pck", 'w')
	pickle.dump(numpy.array(test_inputs), f)
	f.close()
	f  = open(savedir + "/dev/" + "dev_inputs.pck", 'w')
	pickle.dump(numpy.array(dev_inputs), f)
	f.close()
	f  = open(savedir + "/dev/" + "dev_targets.pck", 'w')
	pickle.dump(numpy.array(dev_targets), f)
	f.close()

	# f = open(savedir + "/train/" + "training_data.pickle", 'w')
	# pickle.dump(zip(train_inputs,train_target), f)
	# f.close()
	# f = open(savedir + "/test/" + "test_data.pickle", 'w')
	# pickle.dump(zip(test_inputs,test_target), f)
	# f.close()




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
