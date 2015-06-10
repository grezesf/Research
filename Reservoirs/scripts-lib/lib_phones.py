#!/usr/bin/python


### README
# library of functions related to the phones of TIMIT

def load_phone_file(phonePath):
    #given a path to TIMIT_phone_list.txt, returns a list of the phones
    phones_list = []
    try:
        f = open(phonePath)
        for line in f:
            phones_list.append(line.split())
        # close f
        f.close()

    except IOError:
        print "missing phone file"

    # flatten the list using nested list comprehension
    return [val for subl in phones_list for val in subl]



def find_phone_index(start_time, phone_times, phone_list, sample_rate=16000.0):
    # given a frame start time, a list of phone times for this audio file, and a list of phones
    # returns the index of the phone corresponding to this frame in the list

    # sample_rate = 16000.0 (16kHz for TIMIT)

    for i in range( len(phone_times[0])):

        # print phone_times[0][i], float(start_time)*sample_rate, phone_times[1][i]

        if float(phone_times[0][i]) <= float(start_time)*sample_rate <= float(phone_times[1][i]):
            return phone_list.index(phone_times[2][i])

    # if nothing matches, return silence
    # this happens when the start time is beyond the last frame
    # see timit doc
    return phone_list.index("h#")