import argparse
import subprocess
import os 
import sys
import glob
import pysam
import re

#Sample name
sample=sys.argv[1]
folder=sys.argv[2]
#Folder with the samples data:
samples_path=folder

#Folder with the reference genome:
refgen_path='../Reference_Genomes/'

print ('ANALYSIS OF SAMPLE:',sample)

#Name of all the samples in the folder:
samples=os.listdir(samples_path)

#Function to parse sam files.

def SAM_iterator(sam_filename):
    """Function that parses a sam file"""
    samfile = pysam.AlignmentFile(sam_filename, "rb")
    for line in samfile:
        #print (line)
        list_read=str(line)
        read=(list_read.split('\t'))
        yield (read)


if sample in samples:
    sample_1=sample.split('.')
    sample_name=sample_1[0]

    if sample_1[1]=='fa' or sample_1[1]=='fastq':

        #####ALIGNMENT WITH THE WHOLE GENOME#######
	
        #In this step we only obtain the bam file directly and only for the mapped reads (https://rnaseqmalta.wordpress.com/2013/09/09/how-to-make-bowtie2-output-as-bam/)
        if not os.path.exists('../Results/'+sample_name+'/Alignment_WG/'):
            os.makedirs('../Results/'+sample_name+'/Alignment_WG/')
        
        print ('1-Performing the Alignment with the whole genome:')
        os.system('bowtie2 --local -p 5 -N 0 -x '+refgen_path+'genome'+' '+samples_path+sample+' --un ../Results/'+sample_name+'/Alignment_WG/'+sample_name+'_unmapped_WGloc.fastq'+' | samtools view -bSF4 - > '+'../Results/'+sample_name+'/Alignment_WG/'+sample_name+'_WGloc_mapped.bam')

        #Set working directory, is going to change for each sample.
        os.chdir('../Results/'+sample_name+'/Alignment_WG/')
		
        ######PROCESSING THE ALIGNMENT FILES: INDEX AND SORTING THE BAM FILES########

        print ('Processing the Alignment Files:')
		
        #Sort the bam file:
        os.system('samtools sort '+sample_name+'_WGloc_mapped.bam'+ ' -o ' +sample_name+'_WGloc_mapped_sort.bam')
		
        #Index
        os.system('samtools index '+sample_name+'_WGloc_mapped_sort.bam')  

        #######OBTAIN THE tRNA READS ONLY##############
		
        #Obtain the reads that correspond to tRNA only:
        print ('4.Obtain the reads that correspond to tRNA only')
        os.system('samtools view -b -L '+'../../../Reference_Genomes/info/tRNA_only.bed'+' '+sample_name+'_WGloc_mapped.bam > '+sample_name+'_WGloc_only_trna.bam')
		
        #Sort and indexing the bam file with the the reads that correspond to tRNA  only:
        print ('5.Sort and indexing the reads that correspond to tRNA  only:')
        os.system('samtools sort '+sample_name+'_WGloc_only_trna.bam'+ ' -o ' +sample_name+'_WGloc_only_trna_sort.bam')
		
        #Index the bam file of tRNA precursor data only:
        os.system('samtools index '+sample_name+'_WGloc_only_trna_sort.bam')

        #######SOFT CLIPPING###### remove clipped bases from a BAM file, clipped bases can be adapter sequences.
        os.system('java -jar ../../../Scripts/jvarkit/dist/biostar84452.jar '+sample_name+'_WGloc_only_trna_sort.bam > '+sample_name+'_WGloc_only_trna_soft_clipped_removed.bam')

        os.system('samtools sort '+sample_name+'_WGloc_only_trna_soft_clipped_removed.bam'+ ' -o ' +sample_name+'_WGloc_only_trna_soft_clipped_removed_sort.bam')

        os.system('samtools index '+sample_name+'_WGloc_only_trna_soft_clipped_removed_sort.bam') 

        #######OBTAIN THE PRECURSOR READS############

        #Extract the reads that correspond to tRNA precursor only. lead_trail.bed contains the trailing regions, if a read falls in to these regions is considered a precursor. 
        print ('6.Extract the reads that correspond to tRNA precursor only (have leading and trailing regions):')
        os.system('samtools view -b -L '+'../../../Reference_Genomes/info/lead_trail_ok.bed '+sample_name+'_WGloc_only_trna_soft_clipped_removed_sort.bam > '+sample_name+'_WGloc_only_trna_precursor.bam')
		
        #Sort the bam file with the the reads that correspond to tRNA precursor only:
        print ('7.Sort and indexing the reads that correspond to tRNA precursor only:')
        os.system('samtools sort '+sample_name+'_WGloc_only_trna_precursor.bam'+ ' -o ' +sample_name+'_WGloc_only_trna_precursor_sort.bam')
		
        #Index the bam file of tRNA precursor data only:
        os.system('samtools index '+sample_name+'_WGloc_only_trna_precursor_sort.bam')   
		
        #Obtain the reads in sam format
        os.system('samtools view -h -o '+sample_name+'_WGloc_only_trna_precursor_sort.sam '+sample_name+'_WGloc_only_trna_precursor_sort.bam')
	
        #Filter the precursor file to detect reads that have a deletion so they don't have the intronic region and they should be mature reads. 
        print ('8.Obtain the tRNA introns that have a deletion, and classify as mature')

        out_id= open(sample_name+'intron_delet_mature.txt',"w")
        count_mapq=0
        all_reads=0
        fd = open(sample_name+'_WGloc_only_trna_precursor_sort.sam',"r")
        for aln in SAM_iterator(fd):
            qname=str(aln[0])
            cigar=str(aln[5])
            seq=str(aln[9])

            #cigar code info: https://drive5.com/usearch/manual/cigar.html
            #We have to look to the cigar code to see if there is a deletion if the deletion (D in the cigar) is higher than 8 nucleotides then we consider that is an intron.

            if 'D' in cigar:
                for num1, i_or_d, num2, m in re.findall('(\d+)([ID])(\d+)?([A-Za-z])?', cigar):
                    if int(num1) > 3:
                        out_id.write(qname+'\n')

			

		
        out_id.close()

        print ('10.Obtain the reads that are precursor only by removing the reads that have been filtered before')

        #change comand line !!!! https://github.com/broadinstitute/picard/wiki/Command-Line-Syntax-Transition-For-Users-(Pre-Transition)
        os.system('PicardCommandLine FilterSamReads '+'I='+sample_name+'_WGloc_only_trna_precursor_sort.bam '+'O='+sample_name+'_WGloc_only_trna_with_intron_precursor.bam READ_LIST_FILE='+sample_name+'intron_delet_mature.txt FILTER=excludeReadList') 

        os.system('samtools sort '+sample_name+'_WGloc_only_trna_with_intron_precursor.bam'+ ' -o ' +sample_name+'_WGloc_only_trna_with_intron_precursor_sort.bam')

        #Index the bam file of tRNA data only:
        os.system('samtools index '+sample_name+'_WGloc_only_trna_with_intron_precursor_sort.bam') 

        #Extract the reads id of the precursor 
        os.system('samtools view -F 4 '+sample_name+'_WGloc_only_trna_with_intron_precursor_sort.bam '+'| cut -f1 | sort -u > '+sample_name+'_WGloc_only_trna_precursor_filtered.txt')

        #Extact the mature reads:
        os.system('PicardCommandLine FilterSamReads '+'I='+sample_name+'_WGloc_only_trna_soft_clipped_removed_sort.bam '+'O='+sample_name+'_WGloc_only_trna_mature.bam READ_LIST_FILE='+sample_name+'_WGloc_only_trna_precursor_filtered.txt FILTER=excludeReadList') 
		
        print ('11.Sort and indexing the reads that correspond to tRNA mature only:')
        os.system('samtools sort '+sample_name+'_WGloc_only_trna_mature.bam'+ ' -o ' +sample_name+'_WGloc_only_trna_mature_sort.bam')
        #Index the bam file of tRNA precursor data only:
        os.system('samtools index '+sample_name+'_WGloc_only_trna_mature_sort.bam')

        #####Obtain the input for the aligment with the mature genome

        print ('12.Obtain the input for the aligment with the mature genome (mature reads + unmapped reads)')
        #Marge the mature file of reads and the unmmaped reads, in order to peform the aligment with the mature genome:
        os.system('bedtools bamtofastq -i '+sample_name+'_WGloc_only_trna_mature.bam -fq '+sample_name+'_WGloc_only_trna_mature.fastq')

        #Marge fastq 
        os.system('cat '+sample_name+'_WGloc_only_trna_mature.fastq '+sample_name+'_unmapped_WGloc.fastq > '+sample_name+'_WGloc_only_trna_mature_and_unmapped.fastq')