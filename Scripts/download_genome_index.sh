#!/bin/bash

cd ..
cd Reference_Genomes
wget http://igenomes.illumina.com.s3-website-us-east-1.amazonaws.com/Homo_sapiens/UCSC/hg38/Homo_sapiens_UCSC_hg38.tar.gz
tar -zxvf Homo_sapiens_UCSC_hg38.tar.gz
mv Homo_sapiens/UCSC/hg38/Sequence/Bowtie2Index/genome.1.bt2 genome.1.bt2
mv Homo_sapiens/UCSC/hg38/Sequence/Bowtie2Index/genome.2.bt2 genome.2.bt2
mv Homo_sapiens/UCSC/hg38/Sequence/Bowtie2Index/genome.3.bt2 genome.3.bt2
mv Homo_sapiens/UCSC/hg38/Sequence/Bowtie2Index/genome.4.bt2 genome.4.bt2
mv Homo_sapiens/UCSC/hg38/Sequence/WholeGenomeFasta/genome.fa genome.fa
mv Homo_sapiens/UCSC/hg38/Sequence/WholeGenomeFasta/genome.dict genome.dict
mv Homo_sapiens/UCSC/hg38/Sequence/WholeGenomeFasta/genome.fa.fai genome.fa.fai
mv Homo_sapiens/UCSC/hg38/Sequence/WholeGenomeFasta/GenomeSize.xml GenomeSize.xml
mv Homo_sapiens/UCSC/hg38/Sequence/Bowtie2Index/genome.fa genome.fa
mv Homo_sapiens/UCSC/hg38/Sequence/Bowtie2Index/genome.rev.1.bt2 genome.rev.1.bt2
mv Homo_sapiens/UCSC/hg38/Sequence/Bowtie2Index/genome.rev.2.bt2 genome.rev.2.bt2
rm Homo_sapiens_UCSC_hg38.tar.gz
rm -r Homo_sapiens
bowtie2-build families_tRNA_refgenome.fa families_tRNA_refgenome
bowtie2-build precursor_tRNA_refgenome.fa precursor_tRNA_refgenome