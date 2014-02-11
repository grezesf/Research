#!/bin/sh

# set -x

# part 4.1 of the paper.
# uncomment desired steps


### Step 1: Feature extraction
# echo "Step 1: Feature extraction"
# # path to TIMIT dataset
# TIMITPath=/home/data/TIMIT/
# # desired path to save the MFCCs
# MFCCPath=~/Research/Reservoirs/datasets/TIMIT-mfccs/
# # path to opensmile exectutable (no trailing /)
# SMILExtractPath=/home/apps/opensmile-1.0.1/SMILExtract
# # path to conf file
# confPath=~/Research/Reservoirs/Task0_Replication/code/preprocessing/MFCC12_E_D_A.conf
# python feat_extract.py $TIMITPath $SMILExtractPath $confPath $MFCCPath


# ### Step 2: calculate rescaling factors
# echo "Step 2: calculate rescaling factors"
# # path to mfccs
# MFCCPath=~/Research/Reservoirs/datasets/TIMIT-mfccs/
# # desired path to save scaling factors
# resultsPath=~/Research/Reservoirs/results/preprocessing/
# python rescaling.py $MFCCPath $resultsPath


# ### Step 3: remake MFCCs using rescaling factors
# echo "Step 3: remake MFCCs using rescaling factors"
# # path to file containing the rescaling factors and averages
# factors=~/Research/Reservoirs/code/preprocessing/factors.csv
# averages=~/Research/Reservoirs/results/preprocessing/averages.csv
# # path to original MFCCs
# MFCCPath=~/Research/Reservoirs/datasets/TIMIT-mfccs/
# # desired path to save rescaled mfccs
# remakePath=~/Research/Reservoirs/datasets/rescaled-TIMIT-mfccs/
# python remakeMFCCs.py $MFCCPath $factors $averages $remakePath


### Step 4: copy over remaining files
# echo "Step 4: copy over remaining files"
# TIMITPath=/home/data/TIMIT/
# remakePath=~/Research/Reservoirs/datasets/rescaled-TIMIT-mfccs/
# cp -r -n $TIMITPath/* $remakePath


# ### Step 5: extract phone list
# echo "Step 5: extract phone list"
# python extract_phone_list.py $TIMITPath $resultsPath


### Step 6: convert to OGER compatible format
# Paths: don't forget / at end
# desired path to save oger compatible files
# OGERdir=~/reservoirs/datasets/oger-compatible-files/ 
# file containing the list of phones
# phoneList=$resultsPath/TIMIT_phone_list.txt
# echo "Step 6: convert to OGER compatible format"
# python convert2oger.py $remakePath $phoneList $OGERdir


### Extra: make dev set
# TIMIT_Dev=~/reservoirs/datasets/TIMIT_Dev/
# Devdir=~/reservoirs/datasets/oger-dev/
# echo "Extra: make dev set"
# python convert2oger.py $TIMIT_Dev $phoneList $Devdir