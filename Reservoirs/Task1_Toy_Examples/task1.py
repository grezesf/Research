import mdp
import Oger
import numpy
import pylab
from lib_task1 import *

### README
# First attempt at a functional reservoir 


### Create reservoir
# construct individual nodes, 
reservoir_size = 100
reservoir = Oger.nodes.ReservoirNode(output_dim=reservoir_size, input_scaling=0.05)
readout = Oger.nodes.RidgeRegressionNode()

# build network with MDP framework
flow = mdp.Flow([reservoir, readout], verbose=1)
Oger.utils.make_inspectable(Oger.nodes.ReservoirNode)

### Create/Load dataset
# Both x and y are lists of 2D numpy arrays. 
# Oger inherets the dimensionality convention from MDP, 
# so the rows represent timesteps and the columns represent different signals.

# Get the dataset using task1_lib
[x, y] = gen_toy_data(data_dim=500, set_size=200, freq_range=[10,100], phase_range=[0,9], amplitude_range=[1,10], delay=15.5)

# print x,y
print numpy.shape(x)
# should be (set_size, data_dim, point_dim) (in this case point_dim=1)
# print x[0][0:10]
print numpy.shape(x[0]),numpy.shape(x[1]),numpy.shape(x[2]),numpy.shape(x[3]),numpy.shape(x[4])
# print numpy.shape(y)


# create MDP format input
data = [None, zip(x[0:-2], y[0:-2])]
# print data

# train the flow 
flow.train(data)

#apply the trained flow to the training data and test data
trainout = flow(x[0])
testout1 = flow(x[-1])
testout2 = flow(x[-2])


print "NRMSE: " + str(Oger.utils.nrmse(y[-1], testout1))

# plot results
nx = 5
ny = 1

# plot a few input_scaling
pylab.subplot(nx, ny, 1)
pylab.plot(x[0])
pylab.subplot(nx, ny, 1)
pylab.plot(x[1])
pylab.subplot(nx, ny, 1)
pylab.plot(x[2])

#plot the input and target
pylab.subplot(nx, ny, 2)
pylab.plot(x[0],'r')
pylab.subplot(nx, ny, 2)
pylab.plot(y[0], 'b')

#plot the training output and target
pylab.subplot(nx, ny, 3)
pylab.plot(y[0],'b')
pylab.subplot(nx, ny, 3)
pylab.plot(trainout, 'g')

#plot the testing output and target
pylab.subplot(nx, ny, 4)
pylab.plot(y[-1],'b')
pylab.subplot(nx, ny, 4)
pylab.plot(testout1, 'g')

#plot the testing output and target
pylab.subplot(nx, ny, 5)
pylab.plot(y[-2],'b')
pylab.subplot(nx, ny, 5)
pylab.plot(testout2, 'g')


# pylab.subplot(nx, ny, 6)
# tmp = numpy.array(reservoir.inspect()[-1])
# print tmp.shape
# tmp.shape = (100, 500)

# pylab.plot(tmp[0])
# pylab.plot(tmp[1])
# pylab.plot(tmp[2])
# pylab.plot(tmp[3])


pylab.show()
