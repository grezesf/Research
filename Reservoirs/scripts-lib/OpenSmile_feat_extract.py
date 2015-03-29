#!/usr/bin/python
import os
import sys
import datetime

# README
# reads a dataset directory, copies the directory structure
# performs a mffc extraction on the audio files
# input:
# DataPath: path to the base of the dataset directory
# SMILExtractPath: path to SMILExtract executable
# ConfPath: path to the SMILExtract configuration file
# targetDir: path the the directory in which the mffcs will be saved
# no output


def main():
    # path to corpus
    DataPath = os.path.abspath(os.path.normpath(sys.argv[1]))
    print 'DataPath:', DataPath
    # hack. the name of the directory will be used to recreate directory structure
    splitword = DataPath.split('/')[-1]
    print 'splitword:', splitword

    # path to necessary files
    # SMILExtract executable
    SMILExtractPath = os.path.abspath(os.path.normpath(sys.argv[2]))
    print 'SMILExtractPath:', SMILExtractPath
    # conf file path
    ConfPath = os.path.abspath(os.path.normpath(sys.argv[3]))
    print 'ConfPath:', ConfPath

    # path to save target
    targetDir = os.path.abspath(os.path.normpath(sys.argv[4]))
    print 'targetDir', targetDir
    # create it if it doesnt exist
    if not os.path.exists(targetDir):
        print "Creating target directory"
        os.makedirs(targetDir)
    # create dataset description
    f = open(targetDir + "/" + "description.txt", 'w')
    # f.write("This directory contains the mffc extractions from the audio files of the TIMIT dataset.\n")
    f.write("This directory was created by /home/felix/Research/Reservoirs/scripts-lib/OpenSmile_feat_extract.py on " + str(datetime.date.today()) + "\n")
    f.close()


    # walk the directories
    for (path, dirs, files) in os.walk(DataPath):
        for file in files:
            if ".wav" in file:
                print "working on: " + file
                print "from path : " + path

                # create copy of data directory structure
                ind = path.split("/").index(splitword)
                newDir = "/".join(path.split('/')[ind+1:])
                # print targetDir + "/" + newDir
                if not os.path.exists(targetDir + "/" + newDir):
                    print "creating sub-directory"
                    os.makedirs(targetDir + "/" + newDir )

                # perform OpenSmile feat extraction on current wav file 
                # 25ms samples every 10ms (Hamming window)
                # 12 mffc feats and 1 energy, plus deltas and accel
                base = file[:-4]
                command = SMILExtractPath + " -C " + ConfPath + " -I " + path + "/" + file + " -O " + targetDir + "/" + newDir + "/" + base + ".feats.csv"
                # print command
                os.system(command)

    # test command
    # file = "/home/felix/reservoirs/datasets/TIMIT/test/dr1/faks0/sa1.wav"
    # command = SMILExtractPath + " -C " + ConfPath + " -I " + file + " -O " + targetDir + "sa1" + ".mfcc.csv"
    # os.system(command)

    # don't return anything
    return None

# Call to main 
if __name__=='__main__':
    main()
