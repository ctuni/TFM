import os

#Changing the directory to download to Reference_Genomes
os.system('cd ..')
os.system('cd Reference_Genomes')
#Downloading the file from illumina and uncompressing it
os.system('wget http://igenomes.illumina.com.s3-website-us-east-1.amazonaws.com/Homo_sapiens/UCSC/hg38/Homo_sapiens_UCSC_hg38.tar.gz')
os.system('tar -zxvf Homo_sapiens_UCSC_hg38.tar.gz')
#Moving all the needed files from their folder to the main Reference_Genomes folder
os.system('mv Homo_sapiens/UCSC/hg38/Sequence/Bowtie2Index/genome.1.bt2 genome.1.bt2')
os.system('mv Homo_sapiens/UCSC/hg38/Sequence/Bowtie2Index/genome.2.bt2 genome.2.bt2')
os.system('mv Homo_sapiens/UCSC/hg38/Sequence/Bowtie2Index/genome.3.bt2 genome.3.bt2')
os.system('mv Homo_sapiens/UCSC/hg38/Sequence/Bowtie2Index/genome.4.bt2 genome.4.bt2')
os.system('mv Homo_sapiens/UCSC/hg38/Sequence/WholeGenomeFasta/genome.fa genome.fa')
os.system('mv Homo_sapiens/UCSC/hg38/Sequence/WholeGenomeFasta/genome.dict genome.dict')
os.system('mv Homo_sapiens/UCSC/hg38/Sequence/WholeGenomeFasta/genome.fa.fai genome.fa.fai')
os.system('mv Homo_sapiens/UCSC/hg38/Sequence/WholeGenomeFasta/GenomeSize.xml GenomeSize.xml')
os.system('mv Homo_sapiens/UCSC/hg38/Sequence/Bowtie2Index/genome.fa genome.fa')
os.system('mv Homo_sapiens/UCSC/hg38/Sequence/Bowtie2Index/genome.rev.1.bt2 genome.rev.1.bt2')
os.system('mv Homo_sapiens/UCSC/hg38/Sequence/Bowtie2Index/genome.rev.2.bt2 genome.rev.2.bt2')
#Deleting the tar.gz file
os.system('rm Homo_sapiens_UCSC_hg38.tar.gz')
#Deleting the rest
os.system('rm -r Homo_sapiens')
#Building indexs of the "genome" from tRNA families and precursor tRNA families
os.system('bowtie2-build families_tRNA_refgenome.fa families_tRNA_refgenome')
os.system('bowtie2-build precursor_tRNA_refgenome.fa precursor_tRNA_refgenome')