# Align the reads that have been classified as tRNA with the mature genome. 

import os 
import sys
import subprocess

fullCmdArguments= sys.argv
argumentList= fullCmdArguments[1:]
dir_path = os.path.dirname(os.path.realpath(__file__))
listdir=os.listdir(dir_path)

fastq=sys.argv[1]
sample_name=(fastq.split('.'))[0]
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path.split('/')
path=dir_path.split('/')
path=path[:-1]
refgen_path=('/').join(path)+'/Reference_Genomes/'

if os.path.exists('../Results/'+sample_name):
	if not os.path.exists('../Results/'+sample_name+'/Alignment_MG'):
			os.makedirs('../Results/'+sample_name+'/Alignment_MG')
	else:
		print ('There is a Results folder for the mature genome alignment already created for this sample ! Maybe the analysis has already been done (Cheek the Results folder)')
else:
	print ('The results folder for this sample has not been created so the first step has not been done ! ')
	raise SystemExit

os.chdir('../Results/'+sample_name+'/Alignment_MG/')

#Now the input is the name of the sample plus _STEP2. Change it 
print ('Performing the aligment with the mature genome')
os.system('bowtie2 --local -p 8 -N 0 -x '+refgen_path+'families_tRNA_refgenome ../Alignment_WG/'+sample_name+'_WGloc_only_trna_mature_and_unmapped.fastq'+' --un '+sample_name+'_unmapped_MGloc.fastq'+' | samtools view -bSF4 - > '+sample_name+'_MGloc_mapped.bam')

#####soft clipping####
os.system('java -jar ../../../Scripts/jvarkit/dist/biostar84452.jar '+sample_name+'_MGloc_mapped.bam > '+sample_name+'_MGloc_mapped_soft_clipped_removed.bam')

#Process the bam file obtained
print ('Process the bam file obtained')

#Sort the bam file:
print ('2.Sorting the bam file:')

os.system('samtools sort '+sample_name+'_MGloc_mapped_soft_clipped_removed.bam'+ ' -o ' +sample_name+'_MGloc_mapped_soft_clipped_removed_sort.bam')

#Index
print ('3.Indexing the bam file:')
os.system('samtools index '+sample_name+'_MGloc_mapped_soft_clipped_removed_sort.bam')   
	
#Join the unmapped with the precursor
os.system('bedtools bamtofastq -i ../Alignment_WG/'+sample_name+'_WGloc_only_trna_with_intron_precursor_sort.bam -fq '+sample_name+'_WGloc_only_trna_with_intron_precursor_sort.fastq')

os.system('cat '+sample_name+'_WGloc_only_trna_with_intron_precursor_sort.fastq '+sample_name+'_unmapped_MGloc.fastq > '+sample_name+'_WGloc_only_trna_precursor_and_MGunmapped.fastq')


