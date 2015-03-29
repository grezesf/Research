import mdp
import Oger
import numpy
import pylab
import random
import math
import wave
import datetime
import os
import cPickle as pickle


def main():

    # directories
    # Nativeness directory
    nat_dir = "/home/data/ComParE2015/Nativeness/"
    print "Nativeness wave directory"
    print nat_dir
    wav_dir = nat_dir + 'wav/'
    print wav_dir

    # directory where the results will be saved
    work_dir = "/home/felix/Research/Reservoirs/Task6-COMPARE15/Nativeness"
    exp_dir = work_dir + '/' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    # create exp dir
    if not os.path.exists(exp_dir):
        print "creating exp sub-directory"
        print exp_dir
        os.makedirs(exp_dir)

    # Create Reservoir
    # construct individual nodes
    print "Constructing MDP reservoir node"
    reservoir_size = 100
    input_scaling = 1
    spectral_radius=0.9
    reservoir = Oger.nodes.ReservoirNode(output_dim=reservoir_size, input_scaling=input_scaling, spectral_radius=spectral_radius)

    # build network with MDP framework
    print "Building network"
    flow = mdp.Flow([reservoir], verbose=0)
    Oger.utils.make_inspectable(Oger.nodes.ReservoirNode)

    # save flow in pickled formed   # dump inputs and outputs to be loaded later 
    f = open(exp_dir + "/reservoir.pck", 'w')
    pickle.dump(reservoir, f)
    f.close()

    # save reservoir parameters
    f = open(exp_dir + "/reservoir_params.txt", 'w')
    f.write("reservoir_size: " + str(reservoir_size) + '\n')
    f.write("input_scaling: " + str(input_scaling) + '\n')
    f.write("spectral_radius: " + str(spectral_radius) + '\n')
    f.close()

    # Read wav files
    # walk the directories
    for (path, dirs, files) in os.walk(wav_dir):
        for file in files:
            # look only at the wav files
            if ".wav" in file and 'test_0001' in file:

                print "Working on: " + file
                spf = wave.open(wav_dir + '/' + file,'r')

                #Extract Raw Audio from Wav File
                signal = spf.readframes(-1)
                signal =  1.0*numpy.fromstring(signal, 'Int16')

                # make signal readable by the reservoir (array of correct size, rescaled)
                signal_max = numpy.amax(numpy.absolute(signal))
                signal = numpy.array([[x/signal_max] for x in signal])
                # print "Shape of waves" , numpy.shape(signal)

                # apply waves to flow
                res = flow(signal)
                # print "Shape of res", numpy.shape(res)

                # save result
                save_name = exp_dir +'/' + file + '.resout.gz'
                numpy.savetxt(save_name, res)

    # plot results
    nx = 2
    ny = 1

    # plot a few inputs
    # pylab.subplot(nx, ny, 1)
    # pylab.plot(signal,'r', label='wav signal')
    # pylab.legend()

    # pylab.subplot(nx, ny, 2)
    # pylab.plot(reservoir.inspect()[0])

    # pylab.show()

    # find first step where all activity >0.01



    # end of main
    return None


# Call to main 
if __name__=='__main__':
    main()