import pysam
import pysamstats
import sys
import os
import ast

####!!!!
from Bio import SeqIO
####!!!!

fullCmdArguments= sys.argv
argumentList= fullCmdArguments[1:]
path = os.path.dirname(os.path.realpath(__file__)).split('/')[:-1]

sample=sys.argv[1].split('.')[0]

if not os.path.exists('../Results/'+sample+'/Base_calling/'):
            os.makedirs('../Results/'+sample+'/Base_calling/')

os.chdir('../Results/'+sample+'/Base_calling')

print (sample)
#We want to obtain the base call for precursor and for mature tRNA so we will need both files.
files=['../Final_results/'+sample+'all_mature_sort.bam','../Final_results/'+sample+'_PGloc_mapped_sort.bam']

#We need to know the precursor length.  We use a dictionary for the length of each precursor tRNA.
prec_length=open('../../../Reference_Genomes/info/precursor_length_dict.txt','r')
prec_length=prec_length.readlines()
prec_length=str(prec_length).replace('["','').replace('"]','')
prec_length=ast.literal_eval(prec_length)

#Load the dictionary of families. In order to use it when we classify the precursor tRNA in families. 
fam=open('../../../Reference_Genomes/info/families_grups/info_families_id_dic.fa','r')

###!!!!!!

#Create dictionary with nucleotide sequence for each family.
family_sequence = SeqIO.to_dict(SeqIO.parse('../../../Reference_Genomes/Modifications_files/Ref_seq/families_tRNA_refgenome.fa', "fasta"))



####!!!!!
fam=fam.readlines()

fam=str(fam).replace('["','').replace('"]','')

#We have s string so we transform it to a dictionary. 
fam=ast.literal_eval(fam)


tRNA_total=open(sample+'_all_base_calling_by_pos_CORRECT_OK.txt','w')
tRNA_total.write('TRNA-POS'+'\t'+'A'+'\t'+'C'+'\t'+'G'+'\t'+'T'+'\t'+'REF-COUNTS'+'\n')



#intron info
tRNA_intron_info=open('../../../Reference_Genomes/info/intron_info.txt','r')

tRNA_intron={}

for e in tRNA_intron_info:
	e=e.replace('\r\n','').split('\t')	
	tRNA_intron[e[0]]=e[1:]

#Correct positions (additional bases)

tRNA_pos_correct=open('../../../Reference_Genomes/Modifications_files/Ref_seq/tRNA-pos_ref_CORRECT.txt','r')

tRNA_pos_ref={}
for e in tRNA_pos_correct:
	e=e.split('\t')[:3]
	trna=e[2]
	trna=trna.split(',')
	for i in trna:
		tRNA_pos_ref[i]=e[1]
		

#We process both files (the mature and the precursor)

for file in files:
	bamfile = pysam.AlignmentFile(file)


	##PILEUP FOR MATURE TRNA##
	###CREATE A DICTIONARY WITH ALL THE TRNA AND THE BASE CALLING FOR EACH POSITION IN THE TRNA########
	#All the info for all the positions in a tRNA.
	
	tRNA_all={}
	tRNA_all_prop={}
	
	bam_type=''
	if 'mature' in file:
		bam_type='mature'
	if 'PG' in file:
		bam_type='precursor'
	
	ref_genome=''

	if 'mature' in file:
		ref_genome='../../../Reference_Genomes/Modifications_files/Ref_seq/families_tRNA_refgenome.fa'
	if 'PG' in file:
		ref_genome='../../../Reference_Genomes/Modifications_files/Ref_seq/precursor_tRNA_refgenome.fa'
	


	file_base_call=open(sample+'_'+bam_type+'_'+'base_calling_CORRECT_OK.txt','w')
	

	#BASE CALLING
	#pysam will give us the base calling for each trna (max_depth is used becouse by default the maximum number of reads that will read in a position is 8000, so we increse the number to a high number in order to have the total number of reads correct in a ceratin position.) 
	for record in pysamstats.stat_variation(bamfile,  fafile=ref_genome,  max_depth=10000000):
		ref_base=record['ref']

		tRNA_info='REF-'+str(record['ref'])+':'+str(record[ref_base])+' '+'A:'+str(record['A'])+' '+'C:'+str(record['C'])+' '+'G:'+str(record['G'])+' '+'T:'+str(record['T'])

		tRNA=record['chrom']
		

		pos=''
		ref=record['ref']
		#Positions of the precursor are not the same as the positions in the mature genome since we have the leading and trailing regions and the introns. So we have to transform the positions from the precursor genome to be like the mature ones. 
		if bam_type=='precursor':
			pos_i=record['pos']
			#take in to acount the leading and trailing regions.
			if pos_i > 49 and pos_i < int(prec_length[tRNA])-50:
				pos=pos_i-49
				
				if tRNA[:-3] in tRNA_intron:
					info_intron=tRNA_intron[tRNA[:-3]]
					start_intron=int(info_intron[0])
					end_intron=int(info_intron[1])
					length_intron=int(info_intron[2])

					if pos > start_intron and pos <= end_intron:
						pos=''
					else:
						if pos > end_intron:
							pos=pos-length_intron
			
				if 'His' in tRNA:
					pos=pos+1

		if bam_type=='mature':
			pos=record['pos']+1

		#La base de referencia esta repetida ya que cuando hemos creado tRNA_info lo hemos anadido, ahora eliminamos para que no este repetida. 

		tRNA_info=tRNA_info.split(' ')
		tRNA_info.remove(str(ref_base)+':'+str(record[ref_base]))
		if pos !='':
			if tRNA in tRNA_all:
				tRNA_all[tRNA][pos]=tRNA_info

			else:
				tRNA_all[tRNA]={}
				tRNA_all[tRNA][pos]=tRNA_info
		
		total_bases=0
			
		

	#SAVE THE RESULTS IN FILES 
	for trna in tRNA_all:
		file_base_call.write('>'+trna+'\n')
		positions=tRNA_all[trna]
		for position in positions:
			file_base_call.write(str(position)+'\t'+str(positions[position])+'\n')

	for trna in tRNA_all:

		
		positions=tRNA_all[trna]

		###!!!!!
		pos_used=[]
		###

		for position in positions:
			bases=positions[position]
			def take_first(elem):
				return elem.split(':')[0][-1]
			
			sorted_bases = sorted(bases, key = take_first)
			sorted_bases=','.join(sorted_bases)
			sorted_bases=sorted_bases.split(',')
			values=''
			ref=''
			for e in bases:
				if 'REF' in e:
					ref=e
			for val in sorted_bases:
				val=val.split(':')[1]
				values=values+val+'\t'
			values=values[:-1]
			
			if bam_type=='precursor':
				trna_fam=fam[trna[:-3]]
				if trna_fam in tRNA_pos_ref:
					correct_pos=tRNA_pos_ref[trna_fam]
					#In the dictionary tRNA pos ref we have for each trna the positions of reference. But we have to take in to account the addition of  the cca tail. That is why we have to add the positions 74,75,76.
					pos=correct_pos+','+'74'+','+'75'+','+'76'
					pos=pos.split(',')
					correct_pos=pos[position-1]

					####!!!!!
					pos_used.append(correct_pos)
					####!!!!!

					tRNA_total.write(trna_fam+':'+str(position)+':'+ref.split(':')[0]+':'+correct_pos+'\t'+values+'\t'+ref.split(':')[1]+'\n')

			else:
				if trna in tRNA_pos_ref:
					correct_pos=tRNA_pos_ref[trna]
					pos=correct_pos+','+'74'+','+'75'+','+'76'
					pos=pos.split(',')
					correct_pos=pos[position-1]

					####!!!
					pos_used.append(correct_pos)
					####!!!!

					tRNA_total.write(trna+':'+str(position)+':'+ref.split(':')[0]+':'+correct_pos+'\t'+values+'\t'+ref.split(':')[1]+'\n')

		#####!!!!!
		
	
		if bam_type=='precursor':
			trna=fam[trna[:-3]]
			pos_ref = tRNA_pos_ref[trna]
			pos_ref = pos_ref.split(',')
			pos = list(range(1, len(pos_ref)+1))
			for e in range(len(pos_ref)):
				if pos_ref[e] not in pos_used:
					values='0'+'\t'+'0'+'\t'+'0'+'\t'+'0'
					ref_nuc_seq=(family_sequence[trna].seq)[e].upper()
					tRNA_total.write(trna+':'+str(pos[e])+':REF-'+ref_nuc_seq+':'+pos_ref[e]+'\t'+values+'\t'+'0'+'\n')
			

		else:
			pos_ref = tRNA_pos_ref[trna]
			pos_ref = pos_ref.split(',')			
			pos = list(range(1, len(pos_ref)+1))
			for e in range(len(pos_ref)):
				if pos_ref[e] not in pos_used:
					values='0'+'\t'+'0'+'\t'+'0'+'\t'+'0'
					ref_nuc_seq=(family_sequence[trna].seq)[e].upper()
					tRNA_total.write(trna+':'+str(pos[e])+':REF-'+ref_nuc_seq+':'+pos_ref[e]+'\t'+values+'\t'+'0'+'\n')
			
		

			