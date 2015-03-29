#!/usr/bin/python


# README
# given a dataset directory, converts the data to a UBM (Universal Background Model using EM)
# then creates adapts individual instances using that UBM


def main():
    # path to corpus
    # DataPath = os.path.abspath(os.path.normpath(sys.argv[1]))
    DataPath = '/home/felix/Research/Reservoirs/datasets/COMPARE15-Nativeness-mfcc'
    print 'DataPath:', DataPath

    # targetDir = os.path.abspath(os.path.normpath(sys.argv[4]))
    targetDir = '/home/felix/Research/Reservoirs/datasets/COMPARE15-Nativeness-UBM'
    print 'targetDir', targetDir
    # create it if it doesnt exist
    if not os.path.exists(targetDir):
        print "Creating target directory"
        os.makedirs(targetDir)
    # create dataset description
    f = open(targetDir + "/" + "description.txt", 'w')
    # f.write("This directory contains the mffc extractions from the audio files of the TIMIT dataset.\n")
    f.write("This directory was created by /home/felix/Research/Reservoirs/scripts-lib/UBM_convert.py on " + str(datetime.date.today()) + "\n")
    f.close()






# Call to main 
if __name__=='__main__':
    main()
