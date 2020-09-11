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

sample=sample.split('.')[0]
print (sample)


if os.path.exists('../Results/'+sample):
	if not os.path.exists('../Results/'+sample+'/Alignment_M1G'):
			os.system('mkdir'+' '+'../Results/'+sample+'/Alignment_M1G')
	else:
		print ('There is a Results folder for the mature genome alignment already created for this sample ! Maybe the analysis has already been done (Cheek the Results folder)')
else:
	print ('The results folder for this sample has not been created so the first step has not been done ! ')
	raise SystemExit

os.chdir('../Results/'+sample+'/Alignment_M1G/')


#Now the input is the name of the sample plus _STEP2. Change it 
print ('Performing the aligment with the mature genome (1 mismatch in the seed)')
os.system('bowtie2 --local -p 8 -N 1 -x '+refgen_path+'families_tRNA_refgenome '+'../Alignment_PG/'+sample+'_unmapped_PGloc.fastq'+' --un '+sample+'_unmapped_MG_1M_loc.fastq'+' | samtools view -bSF4 - > '+sample+'_MG_1M_loc_mapped.bam')

os.system('samtools sort '+sample+'_MG_1M_loc_mapped.bam'+ ' -o ' +sample+'_MG_1M_loc_mapped_sort.bam')

#####soft clipping####
os.system('java -jar /home/cris/jvarkit/dist/biostar84452.jar '+sample+'_MG_1M_loc_mapped_sort.bam > '+sample+'_MG_1M_loc_mapped_soft_clipped_removed.bam')

#Process the sam file obtained
print ('Process the bam file obtained')

#Sort the bam file:
print ('2.Sorting the bam file:')
os.system('samtools sort '+sample+'_MG_1M_loc_mapped_soft_clipped_removed.bam'+ ' -o ' +sample+'_MG_1M_loc_mapped_soft_clipped_removed_sort.bam')
	
#Index
print ('3.Indexing the bam file:')
os.system('samtools index '+sample+'_MG_1M_loc_mapped_soft_clipped_removed_sort.bam')   

print ('Obtain the final files')

#Merge the files for mature tRNA
os.system('samtools merge '+'../Final_results/'+sample+'all_mature.bam ../Alignment_M1G/'+sample+'_MG_1M_loc_mapped_soft_clipped_removed_sort.bam '+'../Alignment_MG/'+sample+'_MGloc_mapped_soft_clipped_removed_sort.bam')

#sort
os.system('samtools sort ../Final_results/'+sample+'all_mature.bam '+ ' -o ' +'../Final_results/'+sample+'all_mature_sort.bam')

#index
os.system('samtools index '+'../Final_results/'+sample+'all_mature_sort.bam')   