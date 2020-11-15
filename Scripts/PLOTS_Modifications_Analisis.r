#! /usr/bin/Rscript

##Modification plots.

list.of.packages <- c("gtools","gdata")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)

library('gtools')
library('gdata')
library('dplyr')
library('plyr')
library('data.table')
library('gridExtra')
library('Rsamtools')
library('ggplot2')
library('devtools')
library('stringr')

### TOTAL COUNTS MATRIX

#Variable with the group of samples to be analysed and the name of the group 
group <- list("SRR646457_brain")
group_name <- "Control"

#Combine the results obtained for each sample and obtain a table with the total for the group of samples.
base_call <- read.delim(paste0("/Volumes/TOSHIBA/TFM/programspython/Results/",group[1],"/Base_calling/",group[1],"_all_base_calling_by_pos_CORRECT_OK.txt"),row.names=NULL)

if (length(group) > 1) {
  for (i in (2:length(group))) {
    #Loop to marge all the results for all the samples.
    trna_total_new <- read.delim(paste0("/Volumes/TOSHIBA/TFM/programspython/Results/",group[i],"/Base_calling/",group[i],"_all_base_calling_by_pos_CORRECT_OK.txt"),row.names=NULL)
    base_call <- bind_rows(base_call,trna_total_new) }}

#Marge results.
total_count<-data.frame(aggregate(cbind((base_call$A),base_call$C,base_call$G,base_call$T,base_call$REF.COUNTS),by=list(TRNA.POS=base_call$TRNA.POS), FUN=sum))

#Split tRNA pos to obtain specific info and rename columns.
result <- data.frame(total_count,do.call(rbind,strsplit(as.character(total_count$TRNA.POS),":")))
colnames(result)<- c("TRNA.POS", "A","C","G","T","REF.COUNTS","tRNA_fam","POS","REF","POS.CON")

#Obtain all the families of trna that we are working with. 
fam_id <- unique(result$tRNA_fam)
as.character(levels(fam_id))
fam_id <- as.character(levels(unique(result$tRNA_fam)))

#Create a data frame to save al the results obtained in a_ref.
all_data<-data.frame()


for (trna in fam_id) {
  a <- result[ result$tRNA_fam == trna, ]
  a<-a[order(as.numeric(as.character(a$POS))),]
  a$sum = rowSums(a[ , c(2:5)], na.rm = T)
  a_ref <- data.frame(a,do.call(rbind,strsplit(as.character(a$REF),"-")))
  a_ref$REF <- NULL
  a_ref$X1 <- NULL
  a_ref <- transform(a_ref, Mod.prop.base=1-(a_ref$REF.COUNTS/a_ref$sum))
  a_ref <- replace(a_ref, is.na(a_ref), 0)
  a_ref_info <- subset(a_ref,select=c(TRNA.POS,tRNA_fam,POS,POS.CON,Mod.prop.base,REF.COUNTS,sum,A,C,G,T))
  all_data<- rbind(all_data, a_ref_info)
}

#Now all_data contains the proportion of modificacion for all the tRNAs.
all_data <- data.frame(all_data,do.call(rbind,strsplit(as.character(all_data$TRNA.POS),"-")))
all_data<- subset(all_data, select=c(TRNA.POS,tRNA_fam,POS,POS.CON,sum,REF.COUNTS,Mod.prop.base,A,C,G,T))

all_data<- transform(all_data, Mod.bases=all_data$sum-all_data$REF.COUNTS)
all_data<- subset(all_data, select=c(TRNA.POS,tRNA_fam,POS,POS.CON,sum,REF.COUNTS,Mod.prop.base,A,C,G,T))

#Save the name of all the tRNA fam.
trna_fam <- unique(all_data$tRNA_fam)

#Plots for each family.
for (fam in trna_fam) {
  by_fam <- as.data.frame(all_data[all_data$tRNA_fam == fam, ])
  by_fam <- transform(by_fam, Mod.bases=by_fam$sum-by_fam$REF.COUNTS)
  length_trna <- length(by_fam$TRNA.POS)
  by_fam <- data.frame(by_fam,do.call(rbind,strsplit(as.character(by_fam$TRNA.POS),":")))
  by_fam_table <- subset(by_fam,select=c(POS,POS.CON,Mod.prop.base,sum,Mod.bases,X3,A,G,C,T))
  colnames(by_fam_table) <- c("Position","Consensus_tRNA_base_position","Modification_ratio","Base_coverage","Mod_bases","Reference","A","G","C","T")
  write.table(by_fam_table,file=paste0("../Results/Modification ratio plots/",group_name,"_",fam,".txt"), sep = "\t", row.names = FALSE)
  df <- read.delim(paste0("/Volumes/TOSHIBA/Results/Modification ratio plots/",group_name,"_",fam,".txt"),header = TRUE)
  
  #Plot for the modification relative to base coverage.
  plot_mod_base <- ggplot(df,aes(x=as.numeric(Position),y=as.numeric(paste(df$Modification_ratio)))) +
    geom_line (size=0.5,color="darkslategray") + 
    ylim (0,1) +
    scale_x_discrete (limits = as.factor(df$Consensus_tRNA_base_position)) +
    theme (axis.text.x = element_text(size=5,angle=90),axis.text.y = element_text( hjust = 1,size=5)) +
    labs (x="Consensus tRNA base position", y ="Modification ratio") +
    theme (axis.title=element_text(size=5)) +
    labs (title = fam, subtitle = "Modifiaction Ratio (Relative to base coverage)")
  #Plot for coverage.
  max_val <- max(df$Base_coverage, na.rm = TRUE)
  plot_cov <- ggplot(df,aes(x=as.numeric(Position),y=as.numeric(paste(df$Base_coverage)))) + 
    geom_line (size=0.5,color="darkslategray") +
    ylim (0,max_val) +
    scale_x_discrete (limits = as.factor(df$Consensus_tRNA_base_position)) +
    theme (axis.text.x = element_text(size=5, angle=90),axis.text.y = element_text( hjust = 1,size=5)) +
    labs (x="Consensus tRNA base position", y ="Base Counts") +
    theme (axis.title=element_text(size=5)) + 
    geom_area (alpha = 1, fill="paleturquoise2") +
    labs (subtitle = "Base Coverage")
  
  #Save plots
  a<- grid.arrange(plot_mod_base, plot_cov, nrow=2)
  ggsave(a, file=paste0("../Results/Modification ratio plots/",group_name,"_",fam,".jpeg"), width = 20, height = 10, units = "cm")
}