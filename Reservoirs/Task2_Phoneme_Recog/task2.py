import mdp
import Oger
import numpy
import cPickle as pickle


### Readme
# Task 2: Phone(eme) recognition using MFCCs with reservoirs

### 1: Load MFCCs in pickled form
print "Loading TIMIT MFCCs in pickled form"
# # training set
# train_inputs = pickle.load(open("/home/felix/Research/Reservoirs/datasets/TIMIT-OGER/train/train_inputs.pck"))
# train_targets = pickle.load(open("/home/felix/Research/Reservoirs/datasets/TIMIT-OGER/train/train_targets.pck"))
# # testing set
# test_inputs = pickle.load(open("/home/felix/Research/Reservoirs/datasets/TIMIT-OGER/test/test_inputs.pck"))
# test_targets = pickle.load(open("/home/felix/Research/Reservoirs/datasets/TIMIT-OGER/test/test_targets.pck"))
# dev set
dev_inputs = pickle.load(open("/home/felix/Research/Reservoirs/datasets/TIMIT-OGER/dev/dev_inputs.pck"))
dev_targets = pickle.load(open("/home/felix/Research/Reservoirs/datasets/TIMIT-OGER/dev/dev_targets.pck"))

# print "shape of train inputs:", numpy.shape(train_inputs)
# print "shape of first train input:", numpy.shape(train_inputs[0])
# print "shape of test inputs:", numpy.shape(test_inputs)
# print "shape of first test input:", numpy.shape(test_inputs[0])
print "nb inputs:", len(dev_inputs)
print "shape of dev first input:", numpy.shape(dev_inputs[0])

# create MDP format input
print "Creating MDP format input"
data = [[], zip(dev_inputs[0:10], dev_targets[0:10]), []]

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

# # Nested dictionary
# gridsearch_parameters = {reservoir:{'input_scaling': mdp.numx.arange(0.1, 0.5, 0.1), 'spectral_radius':mdp.numx.arange(0.6, 1.3, 0.2), '_instance':range(5)}}

# # define optimizer
# opt = Oger.evaluation.Optimizer(gridsearch_parameters, Oger.utils.nrmse)

# # Do the grid search
# opt.grid_search(data, flow, cross_validate_function=Oger.evaluation.n_fold_random, n_folds=5)

# train the flow 
flow.train(data)

# # Get the optimal flow and run cross-validation with it 
# opt_flow = opt.get_optimal_flow(verbose=True)

# print 'Performing cross-validation with the optimal flow. Note that this error can be slightly different from the one reported above due to another division of the dataset. It should be more or less the same though.'

# errors = Oger.evaluation.validate(data, opt_flow, Oger.utils.nrmse, cross_validate_function=Oger.evaluation.n_fold_random, n_folds=5)
# print 'Mean error over folds: ' + str(numpy.mean(errors))




# apply the trained flow to the training data and test data
# trainout = flow(train_inputs[0])
# testout = flow(test_inputs[0])
trainout = flow(dev_inputs[0])
testout = flow(dev_inputs[-1])
# print numpy.shape(testout)


## Plotting
nx = 2
ny = 1

# import pylab
import matplotlib.pyplot as plt
from matplotlib import cm

plt.subplot(nx, ny, 1)
plt.imshow(dev_targets[-1].transpose(), interpolation='nearest', cmap=cm.binary)
plt.subplot(nx, ny, 2)
plt.imshow(testout.transpose(), interpolation='nearest', cmap=cm.binary)
# plt.subplot(nx, ny, 3)
# plt.plot(dev_targets[-1])
# plt.subplot(nx, ny, 4)
# plt.plot(testout)
plt.show()
