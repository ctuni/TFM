import os
import subprocess as sp
output = str(sp.getoutput('whoami'))
user=output.split("\\",1)[1]




#sp.call(["/usr/bin/Rscript", "--vanilla", "DEG_analysis.r"])

