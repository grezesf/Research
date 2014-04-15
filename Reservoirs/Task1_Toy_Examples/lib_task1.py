#!/usr/bin/python
import random
import math
import numpy



def gen_toy_data(data_dim=500, set_size=100, freq_range=[20,40], phase_range=[20,40], amplitude_range=[10,50], delay=5, input_noise=0.0, target_noise=0.0):
    # generates toy wavy data
    # data_dim is the number of points per wave 
    # set_size is the number of waves
    # the target is delayed by delay

    # sets starts empty
    input_set = []
    target_set = []

    # set ranges extrema
    [min_freq, max_freq] =  freq_range
    [min_phase, max_phase] = phase_range
    [min_amplitude,max_amplitude] = amplitude_range


    # generate set_size signals
    for nb in range(set_size):

        input_wave = []
        target_wave = []

        # pick random freq, phase and amplitude
        freq1 = random.randint(min_freq, max_freq)
        phase1 = random.randint(min_phase, max_phase)
        amplitude1 = random.randint(min_amplitude,max_amplitude)
        # amplitude1 = 1.0
        freq2 = random.randint(min_freq, max_freq)
        phase2 = random.randint(0, freq2)
        amplitude2 = random.random()

        # test: remove randomness
        # freq1 = 25
        # phase1 = 0
        # amplitude1 = 10


        # generate a signal of data_dim points
        for i in range(data_dim):
            # generate data point
            # generate input noise
            noise = input_noise * (2.0*random.random()-1.0)
                
            point1 = noise + amplitude1 * math.sin(2.0*math.pi*(i+phase1)/freq1)
            point2 = noise + amplitude2 * math.sin(2.0*math.pi*(i+phase2)/freq2)
            
            # add to input_wave
            input_wave.append(numpy.array([point1]))

            # input_wave.append([point1, point2])
            # test: make inputs different sizes
            # if random.random()<0.5:
            #     input_wave.append(numpy.array([point1]))
            # else:
            #      input_wave.append(numpy.array([point1, point1]))

            # generate target point delayed
            if i<delay:
                target1 = 0
                target2 = 0
            else:
                # generate target noise
                noise = target_noise * (2.0*random.random()-1.0)
                target1 = noise + amplitude1 * math.sin(2.0*math.pi*(i+phase1-delay)/freq1)
                target2 = noise + amplitude2 * math.sin(2.0*math.pi*(i+phase2-delay)/freq2)
            
            # add to target_wave
            # target_wave.append([target1, target2])
            target_wave.append(numpy.array([target1]))

        # add signals to data sets
        input_set.append(numpy.array(input_wave))
        target_set.append(numpy.array(target_wave))

    return numpy.array([input_set, target_set])
