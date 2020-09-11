import os

os.system('curl -O https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh')
os.system('sha256sum Anaconda3-2020.07-Linux-x86_64.sh')
os.system('bash Anaconda3-2020.07-Linux-x86_64.sh')
os.system('source ~/.bashrc')
os.system('conda install -c bioconda bowtie2')
os.system('conda install -c bioconda samtools')
os.system('conda install -c bioconda bedtools')