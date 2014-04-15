import mdp
import Oger
import numpy
import pylab
import random
import math

### README
# the goal is to teach the reservoir to recreate the input signal with a certain delay


def main():

    ### Create/Load dataset
    set_size=200
    data_length=500
    delay=100
    [x, y] = gen_random_data(set_size, data_length, delay)
    # print x,y
    print numpy.shape(x)
    # should be (set_size, data_dim, point_dim) (in this case point_dim=1)
    # print x[0][0:10]
    print numpy.shape(x[0]),numpy.shape(x[1]),numpy.shape(x[2]),numpy.shape(x[3]),numpy.shape(x[4])
    # print numpy.shape(y)

    # create MDP format input
    data = [None, zip(x, y)]
    # print data

    ### Create reservoir
    # construct individual nodes, 
    reservoir_size = 200
    reservoir = Oger.nodes.ReservoirNode(output_dim=reservoir_size, input_scaling=0.05)
    readout = Oger.nodes.RidgeRegressionNode()

    # build network with MDP framework
    flow = mdp.Flow([reservoir, readout], verbose=1)
    Oger.utils.make_inspectable(Oger.nodes.ReservoirNode)

    # train the flow 
    flow.train(data)

    #apply the trained flow to the training data and test data
    trainout = flow(x[0])

    # gen test data
    set_size=2
    [x_test, y_test] = gen_random_data(set_size, data_length, delay)
    print numpy.shape(x_test)
    # should be (set_size, data_dim, point_dim) (in this case point_dim=1)
    # print x[0][0:10]
    print numpy.shape(x_test[0]),numpy.shape(x_test[1])

    testout1 = flow(x_test[0])
    testout2 = flow(x_test[1])

    print "NRMSE: " + str(Oger.utils.nrmse(y_test[0], testout1))


    # plot results
    nx = 5
    ny = 1

    # plot a few inputs
    pylab.subplot(nx, ny, 1)
    pylab.plot(x[0],'r')
    pylab.subplot(nx, ny, 1)
    pylab.plot(x[1],'b')
    pylab.subplot(nx, ny, 1)
    pylab.plot(x[2],'g')

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
    pylab.plot(y_test[0],'b')
    pylab.subplot(nx, ny, 4)
    pylab.plot(testout1, 'g')

    #plot the testing output and target
    pylab.subplot(nx, ny, 5)
    pylab.plot(y_test[1],'b')
    pylab.subplot(nx, ny, 5)
    pylab.plot(testout2, 'g')

    pylab.show()

    # end of main
    return None



# data generating function
def gen_random_data(set_size=100, data_length=500, delay=20):
    # set_size is the number of waves
    # data_length is the number of points per wave 
    # the target is delayed by delay

    # sets starts empty
    input_set = []
    target_set = []

    # generate set_size signals
    for nb in range(set_size):

        # waves start empty
        input_wave = [numpy.array([2.0*random.random()-1.0]) for x in range(data_length)]
        target_wave = [numpy.array([0]) for x in range(delay)]
        target_wave.extend(input_wave[:-delay])

        input_set.append(numpy.array(input_wave))
        target_set.append(numpy.array(target_wave))

    return numpy.array([input_set, target_set])


# Call to main 
if __name__=='__main__':
    main()