import os
import sys
import argparse
import subprocess
import glob
import pysam
import re

genome=sys.argv[1]
basename=sys.argv[2]

os.system('bowtie2-build -f --large-index '+genome+' '+basename)