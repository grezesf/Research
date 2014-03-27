import mdp
import Oger
import numpy
import cPickle as pickle


### Readme
# Task 2: Phone(eme) recognition using MFCCs with reservoirs

### 1: Load MFCCs in pickled form
print "Loading TIMIT MFCCs in pickled form"
# training set
train_inputs = pickle.load(open("/home/felix/Research/Reservoirs/datasets/TIMIT-OGER/train/train_inputs.pck"))
train_targets = pickle.load(open("/home/felix/Research/Reservoirs/datasets/TIMIT-OGER/train/train_targets.pck"))
# testing set
test_inputs = pickle.load(open("/home/felix/Research/Reservoirs/datasets/TIMIT-OGER/test/test_inputs.pck"))
test_targets = pickle.load(open("/home/felix/Research/Reservoirs/datasets/TIMIT-OGER/test/test_targets.pck"))
# dev set
# inputs = pickle.load(open("/home/felix/Research/Reservoirs/datasets/TIMIT-OGER/dev/dev_inputs.pck"))
# targets = pickle.load(open("/home/felix/Research/Reservoirs/datasets/TIMIT-OGER/dev/dev_targets.pck"))

# print "shape of train inputs:", numpy.shape(train_inputs)
# print "shape of first train input:", numpy.shape(train_inputs[0])
# print "shape of test inputs:", numpy.shape(test_inputs)
# print "shape of first test input:", numpy.shape(test_inputs[0])
print "nb inputs:", len(train_inputs)
print "shape of dev first input:", numpy.shape(train_inputs[0])

### 2: Create reservoir
# construct individual nodes
print "Constructing reservoir node and readout node"
reservoir_size = 100
reservoir = Oger.nodes.ReservoirNode(output_dim=reservoir_size)
readout = Oger.nodes.RidgeRegressionNode()
wtanode = Oger.nodes.WTANode()

# build network with MDP framework
print "Building network"
flow = mdp.Flow([reservoir, readout, wtanode], verbose=0)
Oger.utils.make_inspectable(Oger.nodes.ReservoirNode)

# create MDP format input
print "Creating test-train data for each node"
data = [[], zip(train_inputs, train_targets), zip(train_inputs, train_targets)]

# Nested dictionary
gridsearch_parameters = {reservoir:{'input_scaling': mdp.numx.arange(0.1, 0.9, 0.1), 'spectral_radius':mdp.numx.arange(0.3, 1.5, 0.1), '_instance':range(5)}}
# gridsearch_parameters = {reservoir:{'_instance':range(5)}}

# define optimizer
opt = Oger.evaluation.Optimizer(gridsearch_parameters, Oger.utils.nrmse)

# Do the grid search
opt.grid_search(data, flow, cross_validate_function=Oger.evaluation.n_fold_random, n_folds=5)

# The corresponding parameter values are, according to pre-run grid search:
# ReservoirNode.input_scaling : 0.1
# ReservoirNode.spectral_radius : 1.2

# Get the optimal flow and run cross-validation with it 
opt_flow = opt.get_optimal_flow(verbose=True)

# print 'Performing cross-validation with the optimal flow. Note that this error can be slightly different from the one reported above due to another division of the dataset. It should be more or less the same though.'

# errors = Oger.evaluation.validate(data, opt_flow, Oger.utils.nrmse, cross_validate_function=Oger.evaluation.n_fold_random, n_folds=5)
# print 'Mean error over folds: ' + str(numpy.mean(errors))

## non grid search verion
# train the flow 
# flow.train(data)

# apply the trained flow to the training data and test data
# trainout = flow(train_inputs[0])
# testout = flow(test_inputs[0])
# trainout = flow(train_inputs[0])
# testout = flow(test_inputs[0])
# print "shape of testout: ", numpy.shape(testout)

import scipy as sp
from Oger.utils import ConfusionMatrix, plot_conf

ytest = []
for xtest in test_inputs:
    ytest.append(opt_flow(xtest))
ymean = sp.atleast_2d(sp.array([sp.argmax(mdp.numx.atleast_2d(mdp.numx.mean(sample, axis=0))) for sample in test_targets])).T
ytestmean = sp.atleast_2d(sp.array([sp.argmax(mdp.numx.atleast_2d(mdp.numx.mean(sample, axis=0))) for sample in ytest])).T

# use ConfusionMatrix to compute some more information about the
confusion_matrix = ConfusionMatrix.from_data(61, ytestmean , ymean) # 61 classes
print "Error rate: %.4f" % confusion_matrix.error_rate # this comes down to 0-1 loss
print "Balanced error rate: %.4f" % confusion_matrix.ber
print

# compute precision and recall for each class vs. all others
print "Per-class precision and recall"
binary_confusion_matrices = confusion_matrix.binary()
for c in range(61):
    m = binary_confusion_matrices[c]
    print "label %d - precision: %.2f, recall %.2f" % (c, m.precision, m.recall)
print

# properties of the ConfusionMatrix and BinaryConfusionMatrix classes can also be used
# as error measure functions, as follows:
ber = ConfusionMatrix.error_measure('ber', 61) # 61-class balanced error rate
print "Balanced error rate: %.4f" % ber(ytestmean, ymean)

# Plotting
import pylab
import matplotlib.pyplot as plt
from matplotlib import cm

# plot confusion matrix (balanced, each class is equally weighted)
pylab.figure()
plot_conf(confusion_matrix.balance())

# nx = 2
# ny = 1

# plt.subplot(nx, ny, 2)
# plt.imshow(dev_targets[-1].transpose(), interpolation='nearest', cmap=cm.binary)
# plt.subplot(nx, ny, 2)
# plt.imshow(testout.transpose(), interpolation='nearest', cmap=cm.binary)
# plt.subplot(nx, ny, 3)
# plt.plot(dev_targets[-1])
# plt.subplot(nx, ny, 4)
# plt.plot(testout)
# plt.show()
