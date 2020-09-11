#!/usr/bin/python

import argparse
import subprocess
import os 
import sys
import glob
import pysam
import re

#usage: python3 download_sra_fastq.py SERIES DOWNLOAD_FOLDER
#example: python3 download_sra_fastq.py GSE114904 ../../sradownload/sra/

series=sys.argv[1]
download_directory=sys.argv[2]

os.system('prefetch '+series)

os.chdir(download_directory)

for filename in glob.glob('*.sra'):
    os.system('fastq-dump '+filename)

#it will take some time