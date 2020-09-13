#!/bin/bash

##Download the file for Linux
curl -O https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh
#Checking the integrity of the file
sha256sum Anaconda3-2020.07-Linux-x86_64.sh
#Running the .sh script
bash Anaconda3-2020.07-Linux-x86_64.sh
#Compiling from source
source ~/.bashrc
rm Anaconda3-2020.07-Linux-x86_64.sh
#Using conda to install bowtie2, samtools and bedtools
conda install -c bioconda bowtie2
conda install -c bioconda samtools
conda install -c bioconda bedtools
#Installing R
sudo apt update
sudo apt -y upgrade
sudo apt -y install r-base
#Installing R packages
sudo apt-get install libcurl4-openssl-dev libxml2-dev
sudo apt-get install libssl-dev
sudo add-apt-repository -y ppa:cran/imagemagick
sudo apt-get update
sudo apt-get install -y libmagick++-dev