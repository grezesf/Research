import mdp
import Oger
import numpy
import pylab
import math
import random

### README
# Here we teach the reservoir to recreate the "SinC" function,
# as is shown in Extreme learning machine: Theory and applications, by Huang et al. 2006


def main():
    # Create Dataset
    set_size = 1000
    [x, y] = gen_sinC_data(set_size, noise=0)
    train_percent = 0.9
    train_size = int(math.floor(train_percent*set_size))
    print numpy.shape(x), numpy.shape(y)
    # print x[:10], y[:10]
    # should be (set_size, data_dim, point_dim) (in this case point_dim=1)


    ### Create reservoir
    # construct individual nodes, 
    reservoir_size = 100
    reservoir = Oger.nodes.ReservoirNode(output_dim=reservoir_size, input_scaling=100)
    readout = Oger.nodes.RidgeRegressionNode()

    # build network with MDP framework
    flow = mdp.Flow([reservoir, readout], verbose=1)
    Oger.utils.make_inspectable(Oger.nodes.ReservoirNode)

    # create MDP format input, no learning in reservoir, only train readout 
    data = [None, zip(x, y)]

    # train the flow 
    flow.train(data)

    # run the reservoir on test data
    # print numpy.shape(flow(x[0]))
    # train_res = [flow(point) for point in x]
    # plot_train_res = [point[:][0] for point in train_res]
    # print numpy.shape(plot_train_res)
    test_res = [flow(i) for i in x[train_size+1:]]
    plot_test_res = [point[:][0] for point in test_res]
    print numpy.shape(test_res), numpy.shape(plot_test_res), numpy.shape(plot_x[train_size+1:])
    train_res = flow(x[0])
    test_res = flow(x[-1])
    # print test_res
    # print test_res[:10]

    # flatten lists for plotting
    plot_y = [point[0][-1] for point in y]
    plot_x = [point[0][-1] for point in x]
    # print plot_x

    # plotting
    nx = 2
    ny = 1

    pylab.subplot(nx, ny, 1)
    pylab.plot(plot_x, plot_y, '+')
    pylab.plot(plot_x, plot_train_res, 'r+')

    # pylab.subplot(nx, ny, 1)
    # pylab.plot(plot_x[train_size+1:] , plot_test_res, '+')
    
    pylab.subplot(nx, ny, 2)
    # pylab.plot(y[0], '+')
    # pylab.plot(train_res, 'r+')
    print numpy.shape(reservoir.inspect()[-1][-1])
    pylab.plot(reservoir.inspect()[-1][-1])
    # pylab.subplot(nx, ny, 3)
    # pylab.plot(y[-1], '+')
    # pylab.plot(test_res, 'r+')

    pylab.show()

    # end of main
    return None


# data generating function
def gen_sinC_data(set_size=5000, noise=0.2, duplicate=1000):

    # sets starts empty
    input_set = []
    target_set = []

    # generate set_size signals
    for nb in range(set_size):

        # commented code was for testing purposes
        input_signal = []
        target_signal = []

        for i in range(200):
            input_point = 0.01*random.random() + 2.0*i/200.0 -1.0

            # generate noisy target
            target_noise = noise*random.random()
            if input_point == 0.0:
                target_point = 100.0 + target_noise
            else:
                target_point = 100.0*(math.sin(10.0*input_point)/(10.0*input_point) + target_noise)

            input_signal.append(numpy.array([input_point]))
            target_signal.append(numpy.array([target_point]))            

        # # generate input
        # input_point = random.randint(-100.0,100.0)/100.0
        # # input_point = 2.0*random.random()-1.0
        # # generate noisy target
        # target_noise = noise*random.random()
        # if input_point == 0.0:
        #     target_point = 1.0 + target_noise
        # else:
        #     target_point = 1.0*(math.sin(10.0*input_point)/(10.0*input_point) + target_noise)

        # # # duplicate values (for testing purposes only)
        # # input_signal = numpy.array([numpy.array([input_point]) for x in range(110)])
        # # target_signal = numpy.array([[0] for x in range(10)] + [numpy.array([target_point]) for x in range(100)])

        # input_signal = numpy.array([numpy.array([input_point])])
        # target_signal = numpy.array([numpy.array([target_point])])

        # # print target_signal

        # # add to datasets
        # input_set.append(numpy.array(input_signal))
        # target_set.append(numpy.array(target_signal))

    # print numpy.shape(input_set)

    return numpy.array([input_set, target_set])


# Call to main 
if __name__=='__main__':
    main()