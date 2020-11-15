#! /usr/bin/Rscript

library(Rsubread)
library( "GenomicAlignments" )
library( "GenomicFeatures" )
library( "Rsamtools" )
library("edgeR")
library("DESeq2")
library("vsn")
library("magick")
library("Glimma")
library("pheatmap")

#Read proportions table
proportions <- read.table("../Results/R_files/Counts_by_gene_total_for_DESeq2.txt", header=TRUE, row.names=1, quote="\"")

options(scipen=999)

# Apply Wilcoxon test (a nonparametric statistical test that compares two paired groups)
test <- apply(proportions,1,function(a)wilcox.test(x=a[1:3],y=a[4:6])$p.value)

test[1:20]


write.table(test, file = "../Results/p-val_iso-trna-cp_CRG.txt", sep = "\t",
            row.names = TRUE, col.names = NA)

options(scipen = 999)

pdf("../Results/heatmap_iso_all_CRG.pdf")

df <- as.data.frame(colData(ntd)["Condition"])

pheatmap(proportions, cluster_rows=T, show_rownames=T, show_colnames = T,
         cluster_cols=FALSE,fontsize_row=0.5, clustering_method="ward")

####MEAN
mean_data <- transform(proportions, Control=(proportions$RC01_Control+proportions$RC02_Control+proportions$RC03_Control)/3)

mean_data <- transform(mean_data, Treated=(proportions$RC05_Treated+proportions$RC06_Treated+proportions$RC08_Treated)/3)
mean_data <- subset(mean_data, select=c(Control,Treated))

pdf("../Results/heatmap_iso_all_CRG_mean.pdf")
pheatmap(mean_data, cluster_rows=T, show_rownames=T, show_colnames = T,
         cluster_cols=FALSE,fontsize_row=0.5, clustering_method="ward.D")

#Differentially expressed genes (TRUE = p-adj < 0.05 | FALSE = p-adj > 0.05)

test_res05 <- test < 0.05
sum <- summary(test_res05)
sum
names(sum)[names(sum) == "FALSE"] <- "[p-adj > 0.05]"
names(sum)[names(sum) == "TRUE"] <- "[p-adj < 0.05]"
names(sum)[names(sum) == "Mode"] <- ""
names(sum)[names(sum) == "logical"] <- "Number of genes"
