# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 14:31:39 2018

@author: soren
"""

### PMID - Abstracts - Aging keywords from Snowmed Extension ###

### Aging keywords found -> Pmid with abstracts ###

## Import packages ##

import os
import re

## Subdirectories ##

Sub_in = "Term lists"
Sub_in2 = "PMID with Abstracts"

Sub_out_main = "PubMed Search"
Sub_out = "PubMed Search/Aging keywords found in abstracts"

#Create folders if they do not exist

try:
    os.mkdir(Sub_out_main)
except Exception:
    pass

try:
    os.mkdir(Sub_out)
except Exception:
    pass

## Files ##

File1 = "Aging keywords.txt"
File2 = "pmid_abstract.txt"

File_out = "Aging_keywords_found_in_abstracts_SNOMED_extension.txt"

## Variables ##

keywords_list = {}
PMID_Abstract = {}
PMID_Found_feature = {}

#For progress

PMID_file_length = 0
#Get number of pmids
with open(os.path.join(Sub_in2,File2), "r",encoding="utf-8") as pmid_file:
    for line in pmid_file:
        PMID_file_length += 1
pmid_file.close

File_line_counter = 0
percentage = 0

## Load list files ##

with open(os.path.join(Sub_in,File1), "r") as feature_file:
    for line in feature_file:
        line = line.strip().split(';')
        keywords_list[line[0]] = line
feature_file.close

#To handle the 22gb large file (pmid with abstract) the file is read and handled on the go.
with open(os.path.join(Sub_in2,File2), "r",encoding="utf-8") as pmid_file:
    for line in pmid_file:
        line = line.strip().split(';')
        #Trying to to find aging terms in abstracts
        
        #Reset variables
        Found_features = [0]*len(keywords_list)
        Counter = 0
        
        #Run through features
        for feature in keywords_list:
            for features in keywords_list[feature]:
                #check if ";" is incorporated in an abstract and handle if present, else search abstracts for features
                if len(line) > 2:
                    for abstract_piece in line[1:]:
                        if features.lower() in abstract_piece.lower():
                            counts = len(re.findall(r'(?=\b{}\b)'.format(features.lower()), line[1].lower()))
                            Found_features[Counter] += counts
                else: 
                    if features.lower() in line[1].lower():
                        counts = len(re.findall(r'(?=\b{}\b)'.format(features.lower()), line[1].lower()))
                        Found_features[Counter] += counts
            #Counter is for saving the count in right order
            Counter += 1
            #Check if any feature is found and skips if none, then converts to 1 or 0 (categorial values)
            if sum(Found_features) > 0:
                Found_features = [1 if x > 0 else 0 for x in Found_features]
                PMID_Found_feature[line[0]] = Found_features
        #Printing progress
        File_line_counter += 1
        if File_line_counter % int(PMID_file_length/100) == 0:
            percentage += 1
            print("Progress: {} / 100 %".format(percentage))
pmid_file.close

print("Search done!")

#Writes the Aging keywords found to a file: Header with mimnumber + features (from feature list)
with open(os.path.join(Sub_out,File_out), "w+") as PMID_Found_feature_file:
    PMID_Found_feature_file.write("PMID;{}\n".format(';'.join(map(str, feature_list.keys())))) 
    for key in PMID_Found_feature:
            PMID_Found_feature_file.write("{};{}\n".format(key, ';'.join(map(str, PMID_Found_feature[key]))))
PMID_Found_feature_file.close

print("File saved.")
