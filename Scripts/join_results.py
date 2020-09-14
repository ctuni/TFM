import os

dir_list=[]
for x in os.listdir('../Results'):
   dir_list=dir_list+[x]

if not os.path.exists('../Results/R_files'):
    os.mkdir('../Results/R_files')

for x in dir_list:
    for y in os.listdir('../Results/'+x+'/Counts'):
        if 'all_total' in y:
            os.system('mv ../Results/'+x+'/Counts/'+y+' ../Results/R_files/'+y)

files_list=[]
for x in os.listdir('../Results/R_files'):
   files_list=files_list+[x]

filenames=[]
for name in files_list:
    name='../Results/R_files/'+name
    filenames=filenames+[name]

with open('../Results/R_files/Counts_by_gene_total_for_DESeq2.txt', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)