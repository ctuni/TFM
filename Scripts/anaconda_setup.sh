#!/bin/bash

curl -O https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh
sha256sum Anaconda3-2020.07-Linux-x86_64.sh
bash Anaconda3-2020.07-Linux-x86_64.sh
source ~/.bashrc
conda install -c bioconda bowtie2
conda install -c bioconda samtools
conda install -c bioconda bedtools