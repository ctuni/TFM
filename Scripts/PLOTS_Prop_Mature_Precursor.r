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


#Variable with the group of samples to be analysed and the name of the group 
group <- list("SRR7216351_HEK293T_Control_CRISPR")
group_name <- "Control"

#Obtain total counts of tRNA aggregating the results of all the samples.
trna_total <- read.delim (paste0("/Volumes/TOSHIBA/TFM/programspython/Results/",group[1],"/Counts/",group[1],"all_total.txt"),row.names=NULL,header = F)

if (length(group) > 1) {
  for (i in (2:length(group))) {
    #Loop to marge all the results of each sample.
    trna_total_new <- read.delim(paste0("/Volumes/TOSHIBA/TFM/programspython/Results/",group[i],"/Counts/",group[i],"all_total.txt"),row.names=NULL,header = F)
    trna_total <- bind_rows(trna_total,trna_total_new) }}
trna_total_all <- data.frame(aggregate(cbind(trna_total$V2), by=list(trna_total$V1), FUN=sum))


#Obtain total counts of mature tRNA aggregating the results of all the samples.
trna_mature <- read.delim(paste0("/Volumes/TOSHIBA/TFM/programspython/Results/",group[1],"/Counts/",group[1],"all_mature_sort.txt"),row.names=NULL,header = F)

if (length(group) > 1){
  for (i in (2:length(group))){
    #Loop to marge all the results of each sample.
    trna_mature_new <- read.delim(paste0("/Volumes/TOSHIBA/TFM/programspython/Results/",group[i],"/Counts/",group[i],"all_mature_sort.txt"),row.names=NULL,header = F)
    trna_mature <- bind_rows(trna_mature,trna_mature_new) }}
trna_mature_all <- data.frame(aggregate(cbind(trna_mature$V3), by=list(trna_mature$V1), FUN=sum))

#Prec vs Mature ratio


trna_total <- data.frame(trna_total_all,do.call(rbind,strsplit(as.character(trna_total_all$Group.1),"-")))
trna_mature <- data.frame(trna_mature_all,do.call(rbind,strsplit(as.character(trna_mature_all$Group.1),"-")))

aa <- levels(trna_total$X2)
aa<- aa[aa !="*"]

#For each family plot by aa.
for (e in aa) {
  trna_total <- data.frame(trna_total_all,do.call(rbind,strsplit(as.character(trna_total_all$Group.1),"-")))
  trna_total <- subset(trna_total,trna_total$X2 !="*")
  
  trna_mature <- data.frame(trna_mature_all,do.call(rbind,strsplit(as.character(trna_mature_all$Group.1),"-")))
  trna_mature <- subset(trna_mature,trna_mature$X2 !="*")
  trna_total_sub <- subset(trna_total,trna_total$X2 ==e)
  trna_mature_sub <- subset(trna_mature,trna_mature$X2 ==e)
  
  trna_prec_mature_group <- transform(trna_total_sub, mature=trna_mature_sub$V1)
  trna_prec_mature_group <- trna_prec_mature_group[c("Group.1","V1","mature")]
  colnames(trna_prec_mature_group)<- c("TRNA.NAME","total", "mature")
  
  #Obtain proportions.
  trna_prec_mature_group <- transform(trna_prec_mature_group, precursor=trna_prec_mature_group$total-trna_prec_mature_group$mature)
  trna_prec_mature_group <- transform(trna_prec_mature_group, precursor.ratio=(trna_prec_mature_group$precursor/trna_prec_mature_group$total))
  trna_prec_mature_group <- transform(trna_prec_mature_group, mature.ratio=(trna_prec_mature_group$mature/trna_prec_mature_group$total))
  
  #Prepare the data to create the plots.
  trna_mature_by_group <- subset(trna_prec_mature_group, select=c(TRNA.NAME,mature.ratio))
  trna_mature_by_group <- transform(trna_mature_by_group, type="Mature")
  trna_prec_by_group <- subset(trna_prec_mature_group, select=c(TRNA.NAME,precursor.ratio))
  trna_prec_by_group  <- transform(trna_prec_by_group , type="Precursor")
  colnames(trna_prec_by_group) <- c("TRNA.NAME","counts", "Type")
  colnames(trna_mature_by_group) <- c("TRNA.NAME","counts", "Type")
  plot_data_by_group <- rbind(trna_prec_by_group, trna_mature_by_group)
  plot_data_by_group <- subset(plot_data_by_group, TRNA.NAME!="* *")
  
  #Create and save the plots.
  p <- ggplot(plot_data_by_group, aes(fill=Type, y=counts, x=TRNA.NAME)) + 
    geom_bar (position="stack", stat="identity",width=0.5) + 
    theme (text = element_text(size=8),axis.text.x = element_text(angle=90, hjust=1,face="bold"),axis.text.y = element_text(face="bold")) +
    ylim (0,1) + 
    labs (x = "tRNA gene", y = "Proportion") + 
    theme (panel.background = element_rect(fill = "snow2",colour = "snow2",size = 0.5, linetype = "solid")) +
    labs (title = "pre-tRNA vs mature tRNA", subtitle = e) + 
    scale_fill_discrete(name = "", labels = c("pre-tRNA", "mature tRNA"))
  p
  ggsave (p, file=paste0("../Results/Counts plots/Mature_vs_Precursor/By_tRNA_gene/",group_name,"_",e,"_by_gene.jpeg"), width = 20, height = 10, units = "cm")
}


#By anticodon
trna_total <- data.frame(trna_total_all,do.call(rbind,strsplit(as.character(trna_total_all$Group.1),"-")))
trna_total <- subset(trna_total,trna_total$X2 !="*")

trna_mature <- data.frame(trna_mature_all,do.call(rbind,strsplit(as.character(trna_mature_all$Group.1),"-")))
trna_mature <- subset(trna_mature,trna_mature$X2 !="*")

trna_mature$trna <- paste(trna_mature$X2,trna_mature$X3)
trna_mature<-data.frame(aggregate(cbind(trna_mature$V1), by=list(trna_mature$trna), FUN=sum))

trna_total$trna <- paste(trna_total$X2,trna_total$X3)
trna_total<-data.frame(aggregate(cbind(trna_total$V1), by=list(trna_total$trna), FUN=sum))
trna_prec_mature <- transform(trna_mature, Total=trna_total$V1)

#Obtain proportions.
colnames(trna_prec_mature) <- c("TRNA.NAME","mature", "total")
trna_prec_mature <- transform(trna_prec_mature, precursor=trna_prec_mature$total-trna_prec_mature$mature)
trna_prec_mature <- transform(trna_prec_mature, precursor.ratio=(trna_prec_mature$precursor/trna_prec_mature$total))
trna_prec_mature <- transform(trna_prec_mature, mature.ratio=(trna_prec_mature$mature/trna_prec_mature$total))

trna_mature <- subset(trna_prec_mature, select=c(TRNA.NAME,mature.ratio))
trna_mature <- transform(trna_mature, type="mature")

trna_prec <- subset(trna_prec_mature, select=c(TRNA.NAME,precursor.ratio))
trna_prec <- transform(trna_prec, type="Precursor")
colnames(trna_prec) <- c("TRNA.NAME","counts", "Type")
colnames(trna_mature) <- c("TRNA.NAME","counts", "Type")
plot_data <- rbind(trna_prec, trna_mature)
plot_data <- subset(plot_data, TRNA.NAME!="Ile GAT")
trna_prec_mature <- subset(trna_prec_mature, TRNA.NAME!="Ile GAT")

p <- ggplot(plot_data, aes(fill=Type, y=counts, x=TRNA.NAME)) + 
  geom_bar (position="stack", stat="identity",width=0.5) + 
  theme (axis.text.x = element_text(angle=90, hjust=1,face="bold", size = 5),axis.text.y = element_text(face="bold", size = 8)) + 
  ylim (0,1) + 
  labs (x = "tRNA isodecoder", y = "Proportion") + 
  theme (panel.background = element_rect(fill = "snow2",colour = "snow2",size = 0.5, linetype = "solid")) +
  labs (title = "pre-tRNA vs mature tRNA", subtitle = "Isodecoder") +
  scale_fill_discrete(name = "", labels = c("pre-tRNA", "mature tRNA"))

p
ggsave(p, file=paste0("../Results/Counts plots/Mature_vs_Precursor/",group_name,"_by_Isodecoder.jpeg"), width = 20, height = 10, units = "cm")


#By amino acid.
trna_prec_mature <- subset(trna_prec_mature, select=c(TRNA.NAME,mature,total,precursor))
trna_prec_mature <- data.frame(trna_prec_mature,do.call(rbind,strsplit(as.character(trna_prec_mature$TRNA.NAME)," ")))

trna_prec_mature<-data.frame(aggregate(cbind(trna_prec_mature$mature,trna_prec_mature$precursor,trna_prec_mature$total), by=list(trna_prec_mature$X1), FUN=sum))
colnames(trna_prec_mature)<- c("TRNA.NAME","mature", "precursor","total")

#Obtain proportions.
trna_prec_mature <- transform(trna_prec_mature,precursor.ratio=(trna_prec_mature$precursor/trna_prec_mature$total))
trna_prec_mature <- transform(trna_prec_mature, mature.ratio=(trna_prec_mature$mature/trna_prec_mature$total))

trna_mature_by_aa <- subset(trna_prec_mature, select=c(TRNA.NAME,mature.ratio))
trna_mature_by_aa <- transform(trna_mature_by_aa, type="mature")
colnames(trna_mature_by_aa)<- c("TRNA.NAME","counts", "Type")

trna_precursor_by_aa <- subset(trna_prec_mature, select=c(TRNA.NAME,precursor.ratio))
trna_precursor_by_aa <- transform(trna_precursor_by_aa, type="precursor")
colnames(trna_precursor_by_aa)<- c("TRNA.NAME","counts", "Type")

plot_data_by_aa <- rbind(trna_precursor_by_aa,trna_mature_by_aa)
plot_data_by_aa <- subset(plot_data_by_aa, TRNA.NAME!="* *")

p <- ggplot(plot_data_by_aa, aes(fill=Type, y=counts, x=TRNA.NAME)) + 
  geom_bar (position="stack", stat="identity",width=0.5) + 
  theme (text = element_text(size=10),axis.text.x = element_text(angle=90, hjust=1,face="bold"),axis.text.y = element_text(face="bold")) + 
  ylim (0,1) + 
  labs (x = "tRNA isoacceptor", y = "Proportion") + 
  theme (panel.background = element_rect(fill = "snow2",colour = "snow2",size = 0.5, linetype = "solid")) +
  labs (title = "pre-tRNA vs mature tRNA", subtitle = "Isoacceptor") + 
  scale_fill_discrete(name = "", labels = c("pre-tRNA", "mature tRNA"))
ggsave(p, file=paste0("../Results/Counts plots/Mature_vs_Precursor/",group_name,"_by_Isoacceptor.jpeg"), width = 20, height = 10, units = "cm")
```

