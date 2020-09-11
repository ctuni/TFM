import os 
import sys
import subprocess

fullCmdArguments= sys.argv
argumentList= fullCmdArguments[1:]
dir_path = os.path.dirname(os.path.realpath(__file__))
listdir=os.listdir(dir_path)
dir_path.split('/')
path=dir_path.split('/')
path=path[:-1]
refgen_path=('/').join(path)+'/Reference_Genomes/'

sample=sys.argv[1]

sample_name=sample.split('.')[0]
print (sample)


if os.path.exists('../Results/'+sample_name):
	if not os.path.exists('../Results/'+sample_name+'/Alignment_PG'):
			os.makedirs('../Results/'+sample_name+'/Alignment_PG')
	else:
		print ('There is a Results folder for the mature genome alignment already created for this sample ! Maybe the analysis has already been done (Cheek the Results folder)')
else:
	print ('The results folder for this sample has not been created so the first step has not been done ! ')
	raise SystemExit

os.chdir('../Results/'+sample_name+'/Alignment_PG/')


#Now the input is the name of the sample plus _STEP2. Change it 
print ('Performing the aligment with the precursor genome')
#os.system('bowtie2 --local -p 8 -N 0 -x '+refgen_path+'precursor_tRNA_refgenome '+sample_name+'_WGloc_only_trna_precursor_and_MGunmapped.fastq'+' --un '+sample_name+'_unmapped_PGloc.fastq'+' --al '+sample_name+'_mapped_PGloc.fastq 1> '+sample_name+'_PGloc.sam 2>bowtie2_ALN_PG.log')
os.system('bowtie2 --local -p 8 -N 0 -x '+refgen_path+'precursor_tRNA_refgenome ../Alignment_MG/'+sample_name+'_WGloc_only_trna_precursor_and_MGunmapped.fastq'+' --un '+sample_name+'_unmapped_PGloc.fastq'+' | samtools view -bSF4 - > '+sample_name+'_PGloc_mapped.bam')

print ('Process the bam file obtained')

#Add the file to final result
if not os.path.exists('../Final_results'):
	os.mkdir('../Final_results')

os.system('cp -R '+sample_name+'_PGloc_mapped.bam'+' ../Final_results/') 

#Sort the bam file:
print ('2.Sorting the bam file:')

os.system('samtools sort '+'../Final_results/'+sample_name+'_PGloc_mapped.bam'+ ' -o ' +'../Final_results/'+sample_name+'_PGloc_mapped_sort.bam')

#Index
print ('3.Indexing the bam file:')
os.system('samtools index '+'../Final_results/'+sample_name+'_PGloc_mapped_sort.bam')


