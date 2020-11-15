#! /usr/bin/Rscript


list.of.packages <- c("devtools","eulerr","ggrepel","VennDiagram")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)

library('knitr')
library('Rsamtools')
library('ggplot2')
library('VennDiagram')
library('eulerr')
library('devtools')
library('RColorBrewer')
library('ggrepel')
library('base')
library('plyr')
library('devtools')
library('stringr')
options(scipen=999)

#Variable with the group of samples to be analysed and the name of the group.
group <- list("SRR1836125_RNA_treated_1","SRR1836126_RNA_treated_2")
group_name <- "Control"

#Combine the results obtained for each sample and obtain a table with the total for the group of samples.
trna_total <- read.delim(paste0("/Volumes/TOSHIBA/TFM/programspython/Results/",group[1],"/Counts/",group[1],"all_total.txt"),row.names=NULL,header = F)

if (length(group) > 1) {
  for (i in (2:length(group))) {
    #Loop to marge all the results for all the samples.
    trna_total_new <- read.delim(paste0("/Volumes/TOSHIBA/TFM/programspython/Results/",group[i],"/Counts/",group[i],"all_total.txt"),row.names=NULL,header = F)
    trna_total <- bind_rows(trna_total,trna_total_new) 
  }
}

#Marge results.
trna_total_all <- data.frame(aggregate(cbind(trna_total$V2), by=list(trna_total$V1), FUN=sum))
trna_total <- data.frame(trna_total_all,do.call(rbind,strsplit(as.character(trna_total_all$Group.1),"-")))


#Create plots for each family classified by amino acid 
aa <- levels(trna_total$X2)
aa <- aa[aa !="*"]

for (e in aa) {
  trna_total_sub <- subset(trna_total,trna_total$X2 ==e)
  p <- ggplot (trna_total_sub, aes (y=as.numeric(V1), x=Group.1)) + 
    geom_bar (stat="identity",width=0.5, fill ='darkturquoise') + 
    theme (text = element_text(size=10),axis.text.x = element_text(angle=90, hjust=1,face="bold"), axis.text.y = element_text(face="bold")) +
    labs (x = "tRNA gene", y = "Counts") + 
    theme (panel.background = element_rect(fill = "snow2", colour = "snow2", size = 0.5, linetype = "solid")) +
    labs (title = "Total sequencing read counts", subtitle = e)
  ggsave (p, file=paste0("../Results/Counts plots/Total/By_tRNA_gene/",group_name,"_",e,"_by_gene.jpeg"), width = 20, height = 10, units = "cm")
}


#Plots by anticodon
trna_total$trna <- paste(trna_total$X2,trna_total$X3)
trna_total_by_anticodon<-data.frame(aggregate(cbind(trna_total$V1), by=list(trna_total$trna), FUN=sum))
trna_total_by_anticodon <- subset(trna_total_by_anticodon,trna_total_by_anticodon$Group.1 !="* *")

p <- ggplot(trna_total_by_anticodon, aes(y=V1, x=Group.1 )) + 
  geom_bar (stat="identity",width=0.5, fill ='darkturquoise') + 
  theme (text = element_text(size=8),axis.text.x = element_text(angle=90, hjust=1,face="bold"),axis.text.y = element_text(face="bold")) + 
  labs (x = "tRNA isodecoder", y = "Counts") + 
  theme (panel.background = element_rect(fill = "snow2",colour = "snow2",size = 0.5, linetype = "solid")) + 
  labs (title = "Total sequencing read counts", subtitle = "Isodecoder")
ggsave(p, file=paste0("../Results/Counts plots/Total/",group_name,"_by_Isodecoder.jpeg"), width = 20, height = 10, units = "cm")


#Plots by aminoacid 
trna_total_by_aa <- data.frame(aggregate(cbind(trna_total$V1), by=list(trna_total$X2), FUN=sum))
trna_total_by_aa <- subset(trna_total_by_aa,trna_total_by_aa$Group.1 !="*")

p <- ggplot(trna_total_by_aa, aes(y=V1, x=Group.1 )) + 
  geom_bar(stat="identity",width=0.5, fill ='darkturquoise') + 
  theme(text = element_text(size=10),axis.text.x = element_text(angle=90, hjust=1,face="bold"), axis.text.y = element_text(face="bold")) + 
  labs(x = "tRNA isoacceptor", y = "Counts") +
  theme(panel.background = element_rect(fill = "snow2",colour = "snow2",size = 0.5, linetype = "solid")) +
  labs(title = "Total sequencing read counts", subtitle = "Isoacceptor")
ggsave(p, file=paste0("../Results/Counts plots/Total/",group_name,"_by_Isoacceptor.jpeg"), width = 20, height = 10, units = "cm")
