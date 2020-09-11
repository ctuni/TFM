#This program connects all the alignment steps### Example: python main_tRNA-seq.py ../RNA_seq_data/DONE/  the folder DONE contains RNA sequencing data

import argparse
import subprocess
import os 
import sys
import glob
import pysam
import re


fastq_folder=sys.argv[1]

files=os.listdir(fastq_folder)


for file in files:
	if file[0:2] != '._':
		file_2=file.split('.')
		if len(file_2)==3:
			file_2=file_2[:2]

		if len(file_2) == 2 or len(file_2)==3:
			if file_2[1]== 'fastq' or file_2[1]=='fa':
				sample_name=file_2[0]
				#print (sample_name)
								
				########Create folders########
				'''if not os.path.exists('../Results/'+sample_name):
					os.system('mkdir ../Results/'+sample_name)
					os.system('mkdir ../Results/'+sample_name+'/Alignment_WG')
					os.system('mkdir ../Results/'+sample_name+'/Alignment_MG')
					os.system('mkdir ../Results/'+sample_name+'/Alignment_PG')
					os.system('mkdir ../Results/'+sample_name+'/Alignment_M1G')
					os.system('mkdir ../Results/'+sample_name+'/Final_results')
					os.system('mkdir ../Results/'+sample_name+'/Counts')
					os.system('mkdir ../Results/'+sample_name+'/Base_calling')'''
			
				#USE THE PROGRAM THAT WE WANT#			
				os.system('python Aln_WG.py '+file+' '+fastq_folder)
				os.system('python Aln_MG.py '+file)
				os.system('python Aln_PG.py '+file)
				os.system('python Aln_M1G.py '+file)
				os.system('python Obtain_counts.py '+file)
				os.system('python pileup_ok.py '+file)
				


				#os.system('python Obtain_counts_QUAL.py '+file)
				#os.system('python Aln_MG_N.py '+file)
			#Else:
				#print ('There is a Results folder already created for the sample:'+sample_name+' Maybe the analysis has already been done (Cheek the Results folder)')
				#raise SystemExit
