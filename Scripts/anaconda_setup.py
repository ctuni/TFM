import os

#Download the file for Linux, altough this script will run only on Windows Subsystem for Linux
os.system('wget https://repo.continuum.io/archive/Anaconda3-2020.11-Linux-x86_64.sh')
#Checking the integrity of the file
os.system('sha256sum Anaconda3-2020.11-Linux-x86_64.sh')
#Running the .sh script
os.system('bash Anaconda3-2020.11-Linux-x86_64.sh')
#Compiling from source
os.system('source ~/.bashrc')
os.system('rm Anaconda3-2020.07-Linux-x86_64.sh')
#Using conda to install bowtie2, samtools and bedtools
os.system('conda install -c bioconda bowtie2')
os.system('conda install -c bioconda samtools')
os.system('conda install -c bioconda bedtools')
