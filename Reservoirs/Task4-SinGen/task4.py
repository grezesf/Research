import mdp
import Oger
import numpy
import pylab
import math
import random

### README
# Here we teach the reservoir to recreate an adjustable sinwave generator,
# as is shown in {Tutorial on training recurrent neural networks, covering BPPT, RTRL, EKF and the "echo state network" approach} by H Jaeger (2002)


def main():
    # Create Dataset
    wave_len = 300
    [x, y] = gen_sinwave_data(wave_len, noise=0)
    print numpy.shape(x), numpy.shape(y)
    # print x[:10], y[:10]
    # should be (set_size, data_dim, point_dim) (in this case point_dim=1)


    ### Create reservoir
    # construct individual nodes, 
    reservoir_size = 20
    reservoir = Oger.nodes.ReservoirNode(output_dim=reservoir_size)
    readout = Oger.nodes.RidgeRegressionNode()

    # build network with MDP framework
    flow = mdp.Flow([reservoir, readout], verbose=1)
    Oger.utils.make_inspectable(Oger.nodes.ReservoirNode)

    # create MDP format input, no learning in reservoir, only train readout 
    data = [None, zip(x, y)]

    # train the flow 
    flow.train(data)

    # run the reservoir on test data
    trainout = flow(x[0])


    # plotting
    nx = 2
    ny = 1

    pylab.subplot(nx, ny, 1)
    pylab.plot(y[0], 'b')

    pylab.subplot(nx, ny, 2)
    pylab.plot(trainout, 'r')

    pylab.show()

    # end of main
    return None



def gen_sinwave_data(wave_len=300, noise=0):

    # generate wave
    input_wave = [numpy.array([0]) for x in range(wave_len)]
    output_wave = [numpy.array([math.sin(x/4.0)/2.0]) for x in range(wave_len)]

    # add to input/output sets
    input_set = numpy.array([input_wave])
    output_set = numpy.array([output_wave])

    # return sets
    return numpy.array([input_set, output_set])


    # generate set_size signals
    # for nb in range(set_size):

    #     # # commented code was for testing purposes
    #     # input_signal = []
    #     # target_signal = []

    #     # for i in range(200):
    #     #     input_point = 0.01*random.random() + 2.0*i/200.0 -1.0

    #     #     # generate noisy target
    #     #     target_noise = noise*random.random()
    #     #     if input_point == 0.0:
    #     #         target_point = 100.0 + target_noise
    #     #     else:
    #     #         target_point = 100.0*(math.sin(10.0*input_point)/(10.0*input_point) + target_noise)

    #     #     input_signal.append(numpy.array([input_point]))
    #     #     target_signal.append(numpy.array([target_point]))            

    #     # generate input 
    #     input_point = 0
    #     # input_point = 2.0*random.random()-1.0
    #     # generate noisy target
    #     target_noise = noise*random.random()
    #     target_point = math.sin(nb)
    #         target_point = 1.0*(math.sin(10.0*input_point)/(10.0*input_point) + target_noise)

    #     # # duplicate values (for testing purposes only)
    #     # input_signal = numpy.array([numpy.array([input_point]) for x in range(110)])
    #     # target_signal = numpy.array([[0] for x in range(10)] + [numpy.array([target_point]) for x in range(100)])

    #     input_signal = numpy.array([numpy.array([input_point])])
    #     target_signal = numpy.array([numpy.array([target_point])])

    #     # print target_signal

    #     # add to datasets
    #     input_set.append(numpy.array(input_signal))
    #     target_set.append(numpy.array(target_signal))

    # print numpy.shape(input_set)


# Call to main 
if __name__=='__main__':
    main()