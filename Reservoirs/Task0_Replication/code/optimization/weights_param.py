#!/usr/bin/python
import os
import sys
import pickle

import Oger

import mdp
import pylab
import math

import scipy as sp


def main():

	# data dir
	data_dir = sys.argv[1]
	# load the data
	# for (path, dirs, files) in os.walk(data_dir):
	# 	for file in files:
	# 		print file
	# 		if file == "train_inputs.pck":
	# 			f = open(path + "/" + file)
	# 			train_inputs = pickle.load(f)
	# 			f.close()
	# 		if file == "train_outputs.pck":
	# 			f = open(path + "/" + file)
	# 			train_outputs = pickle.load(f)
	# 			f.close()
	# 		if file == "test_inputs.pck":
	# 			f = open(path + "/" + file)
	# 			test_inputs = pickle.load(f)
	# 			f.close()
	# 		if file == "test_outputs.pck":
	# 			f = open(path + "/" + file)
	# 			test_outputs = pickle.load(f)
	# 			f.close()


	train_inputs = [[1,1,1,1],[2,2,2,2],[3,3,3,3]]
	train_outputs = [[1,-1],[1,-1],[-1,1]]
	test_inputs = [[1,1,2,2]]
	# print train_inputs


	# encapsulate 
	# train_inputs = [train_inputs]
	# test_inputs  = [test_inputs]
	# train_outputs= [train_outputs]
	# test_outputs = [test_outputs]


	# reservoir parameters
	input_dim = len(train_inputs[0])
	print "input_dim = ", input_dim
	print "nb train points =", len(train_inputs)
	output_dim = 1000 # nb of neurons 
	spectral_radius = 0.4
	input_scaling = 0.4
	nonlin_func = math.log
	leak_rate = 0.4647385714 # from figure 3

	# reservoir node
	reservoir_node_1 = Oger.nodes.LeakyReservoirNode(leak_rate=leak_rate, input_dim=input_dim, output_dim=output_dim, spectral_radius=spectral_radius, nonlin_func=nonlin_func, input_scaling=input_scaling)
	
	#readout node
	readout_node_1 = Oger.nodes.WTANode()

	# create flow
	flow_1 = mdp.Flow([reservoir_node_1, readout_node_1])


	print "Training..."

	# print len(zip(train_inputs, train_outputs))
	# print len(zip(train_inputs, train_outputs)[0])
	# print len(zip(train_inputs, train_outputs)[0][0])

	print zip(train_inputs, train_outputs)
	flow_1.train([None, zip(train_inputs, train_outputs)])

	print "Applying to testset..."
	# ytest = []
	# print type(test_inputs)
	# print type(test_inputs[0])
	# print type(test_inputs[0][0])
	# print type(test_inputs[0][0][0])

	for xtest in test_inputs:
		print xtest
		print flow_1(xtest)
		# ytest.append(flow_1(xtest))
	
	# print "Error : " + str(mdp.numx.mean([loss_01_time(sample, target) for (sample, target) in zip(ytest, test_outputs)]))


# Call to main 
if __name__=='__main__':
    main()