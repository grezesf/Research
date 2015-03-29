import mdp
import Oger
import numpy
import pylab
import random


### README
# study the memory capacities of same size reservoirs


def main():

    num_waves = 100
    waves = [gen_test_wave(2.0*random.random()-1.0) for x in range(num_waves)]
    print "Shape of waves" , numpy.shape(waves[0])

    ### Create reservoir
    # construct individual nodes, 
    reservoir_size = 100
    reservoir = Oger.nodes.ReservoirNode(output_dim=reservoir_size, spectral_radius=1.001)
    # readout = Oger.nodes.RidgeRegressionNode()

    # build network with MDP framework
    # flow = mdp.Flow([reservoir, readout], verbose=1)
    flow  = mdp.Flow([reservoir], verbose=1)
    Oger.utils.make_inspectable(Oger.nodes.ReservoirNode)

    # apply waves to flow
    results = [flow(x) for x in waves]
    print "Shape of res", numpy.shape(results[0])
    print "Shape of reservoir.inspect()", numpy.shape(reservoir.inspect())


    # print some results
    # find first step with values all <0.01
    # avg = 0
    # for trace in reservoir.inspect():
    #     # print "memory:", measure_memory(trace)-20
    #     avg += measure_memory(trace)-20.0
    # print "memory average of this reservoir:", avg/num_waves

    # plotting parameters
    nx = 5+1
    ny = 1

    # #plot the input
    for wave in waves:
        pylab.subplot(nx, ny, 1)
        pylab.plot(wave)

    # plot the activity for first 5 inputs
    for num in range(5):
        pylab.subplot(nx, ny, num+2)
        pylab.plot(reservoir.inspect()[num])

    pylab.show()

    # end of main
    return None



def gen_test_wave(max_value = 1):
    # generates a 1D test wave
    # simple step function

    # tunable parameters
    # the max value attained by the wave
    # how long the data stays at 0 at the start
    startup_time = 10
    # how long the data stays at 0 at the end
    cooldown_time = 79
    # how long the signal will be active
    active_time = 11

    wave = [numpy.array([0]) for x in range(startup_time)] 
    wave += [numpy.array([max_value]) for x in range(active_time)] 
    wave += [numpy.array([0]) for x in range(cooldown_time)]

    return numpy.array(wave)


def measure_memory(signal):
    # given a reservoir activity matrix for a given signal, find the first step where all activity<0.01
    # for testing purpose only

    # step count starts at 0
    step = 15


    for frame in signal[15:]:
        if all(i<0.01 and i>-0.01 for i in frame):
            # found the first frame where activity died off
            return step
        else:
            step += 1

    # fail case    
    return None


# Call to main 
if __name__=='__main__':
    main()