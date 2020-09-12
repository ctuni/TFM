import os 
import sys
import subprocess
import ast

fullCmdArguments= sys.argv
argumentList= fullCmdArguments[1:]
path = os.path.dirname(os.path.realpath(__file__)).split('/')[:-1]

sample=sys.argv[1].split('.')[0]

if not os.path.exists('../Results/'+sample+'/Counts/'):
            os.makedirs('../Results/'+sample+'/Counts/')

os.chdir('../Results/'+sample+'/Counts/')
print (sample)
print ('Obtaining counts')
#Obtain counts for mature tRNA.
os.system('samtools idxstats '+'../Final_results/'+sample+'all_mature_sort.bam >'+sample+'all_mature_sort.txt')

#Obtain counts for precuror tRNA.
os.system('samtools idxstats '+'../Final_results/'+sample+'_PGloc_mapped_sort.bam >'+sample+'all_precursor_sort.txt')

########Obtain the total number of counts for each family taking in to account the precursor tRNA that we have for each family.
#Open dictionary of families for each tRNA (tRNA: familyID). The key of the dictionary is the id of a precursor tRNA and the values is the family of the precursor. 
fam=open('../../../Reference_Genomes/info/families_grups/info_families_id_dic.fa','r')

fam=fam.readlines()

fam=str(fam).replace('["','').replace('"]','')

#We have s string so we transform it to a dictionary. 
fam=ast.literal_eval(fam)

mature_counts=open(sample+'all_mature_sort.txt','r')
precursor_counts=open(sample+'all_precursor_sort.txt','r')

total_counts={}

for trna in mature_counts:
	trna=trna.split('\t')
	total_counts[trna[0]]=trna[2]

for trna in precursor_counts:
	trna=trna.split('\t')
	trna_id=str(trna[0][0:-3])
	if trna_id.startswith('tRNA'):
		fam_trna=fam[trna_id]
		if fam_trna in total_counts:
			total_counts[fam_trna]=int(total_counts[fam_trna])+int(trna[2])

total=open(sample+'all_total.txt','w')

for trna in total_counts:
	total.write(trna+'\t'+str(total_counts[trna])+'\n')
