#!/bin/sh

# set -x

# part 4.1 of the paper.
# uncomment desired steps


# ### Step 1: Feature extraction
# echo "Step 1: Feature extraction"
# # path to TIMIT dataset
# TIMITPath=/home/data/TIMIT/
# # desired path to save the MFCCs
# featDir=/home/felix/Research/Reservoirs/datasets/TIMIT-mfccs/
# # path to opensmile exectutable (no trailing /)
# SMILExtractPath=/home/apps/opensmile-1.0.1/SMILExtract
# # path to conf file
# confPath=/home/felix/Research/Reservoirs/code/preprocessing/MFCC12_E_D_A.conf
# python feat_extract.py $TIMITPath $SMILExtractPath $confPath $featDir


### Step 2: calculate rescaling factors
echo "Step 2: calculate rescaling factors"
# path to mfccs
MFCCPath=/home/felix/Research/Reservoirs/datasets/TIMIT-mfccs/
# desired path to save scaling factors
resultsPath=/home/felix/Research/Reservoirs/results/preprocessing/
python rescaling.py $MFCCPath $resultsPath


# ### Step 3: remake MFCCs using rescaling factors
# # path to file containing the rescaling factors and averages
# factors=/home/felix/reservoirs/code/preprocessing/factors.csv
# averages=/home/felix/reservoirs/code/preprocessing/averages.csv
# # Paths: don't forget / at end
# # desired path to save rescaled mfccs
# remakePath=/home/felix/reservoirs/datasets/rescaled-mfccs/
# echo "Step 3: remake MFCCs using rescaling factors"
# python remakeMFCCs.py $MFCCPath $factors $averages $remakePath


# ### Step 4: copy over remaining files
# echo "Step 4: copy over remaining files"
# cp -r $TIMITPath/* $remakePath


# ### Step 5: extract phone list
# echo "Step 5: extract phone list"
# python extract_phone_list.py $TIMITPath $resultsPath


### Step 6: convert to OGER compatible format
# Paths: don't forget / at end
# desired path to save oger compatible files
# OGERdir=/home/felix/reservoirs/datasets/oger-compatible-files/ 
# file containing the list of phones
# phoneList=$resultsPath/TIMIT_phone_list.txt
# echo "Step 6: convert to OGER compatible format"
# python convert2oger.py $remakePath $phoneList $OGERdir


### Extra: make dev set
# TIMIT_Dev=/home/felix/reservoirs/datasets/TIMIT_Dev/
# Devdir=/home/felix/reservoirs/datasets/oger-dev/
# echo "Extra: make dev set"
# python convert2oger.py $TIMIT_Dev $phoneList $Devdir