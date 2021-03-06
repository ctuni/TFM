#! /usr/bin/Rscript

# PIPELINE FOR DIFFERENTIAL EXPRESION ANALYSIS FOR LINUX

list.of.packages <- c("magick","pheatmap","BiocManager")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)

list.of.packages <- c("Rsubread", "GenomicAlignments","GenomicFeatures","Rsamtools", "edgeR", "DESeq2","vsn","Glimma")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) BiocManager::install(new.packages)

rm(list.of.packages)
rm(new.packages)

library(Rsubread)
library("GenomicAlignments")
library("GenomicFeatures")
library("Rsamtools")
library("edgeR")
library("DESeq2")
library("vsn")
library("magick")
library("Glimma")
library("pheatmap")

#1-Obtain count matrix.
tmp_total <- read.delim("../Results/R_files/Counts_by_gene_total_for_DESeq2.txt",row.names = 1)
tmp_total

#2-Obtain sample info.
sampleInfo_total <- read.delim("../Results/R_files/sample_data.txt")

#3-Use the count matrix and the sample info to create the final matrix.
deseqdata_total <- DESeqDataSetFromMatrix(countData=tmp_total, colData=sampleInfo_total, design=~Condition)
deseqdata_total

## Samples 
sampleInfo_total
table(deseqdata_total$Condition)

## Sequencing depth

##Remember:The DESeq2 model internally corrects for library size, so transformed or normalized values such as counts scaled by library size should not be used as input.

sum(colSums(assays(deseqdata_total)$counts)) #all the reads of the whole experiment 
sum(colSums(assays(deseqdata_total)$counts))/ncol(deseqdata_total) #this is the ideal depth (is the same value as the mean of the summary)
dge <- DGEList(counts=assays(deseqdata_total)$counts, genes=mcols(deseqdata_total))
ord <- order(dge$samples$lib.size/1e6)

##Sequencing depth plot
pdf('../Results/barplot.pdf')
barplot(dge$samples$lib.size[ord]/1e6, las=1, ylab="Millions of reads",
        xlab="Samples", col=c("cadetblue1", "salmon1")[(deseqdata_total$Condition[ord] == "Treated") + 1], main="Sequencing depth in subset data")
legend("topleft", c("Treated", "Control"), fill=c("cadetblue1", "salmon1"), inset=0.01)

## PCA plots (Samples clustering)
vsd <- varianceStabilizingTransformation(deseqdata_total, blind=FALSE)
rld <- rlog(deseqdata_total, blind=FALSE)
# this gives log2(n + 1)
ntd <- normTransform(deseqdata_total)
dev.off()
pdf("../Results/PCA_plot.pdf")

plotPCA(vsd, intgroup=c("Condition"), returnData= T)

plotPCA(vsd, intgroup=c("Condition"))

## DESeq2

#Level factors 
deseqdata_total$Condition <- factor(deseqdata_total$Condition, levels = c("Treated","Control"))
deseqdata_total$Condition <- droplevels(deseqdata_total$Condition)

#Perform the DE 
des <- DESeq(deseqdata_total)
des$sizeFactor

#CHANGE/VERIFY THE ORDER OF THE COMPARISON
#EXAMPLE: condition ADAT2 vs CONTROL, tells you that the estimates are of the logarithmic fold change log2(ADAT2/CONTROL)
res <- results(des, contrast=c("Condition", "Treated", "Control"),  pAdjustMethod="BH")

write.table(res, file = "../Results/Conditions_Result.txt", sep = "\t",
            row.names = TRUE, col.names = NA)

#We can order our results table by the smallest p value:
resOrdered <- res[order(res$pvalue),]
dev.off()
pdf("../Results/heatmap_total.pdf")

pheatmap(assay(ntd), cluster_rows=T, show_rownames=T, show_colnames = T,
         cluster_cols=FALSE,fontsize_row=0.5, clustering_method="ward.D")

write.table(assay(ntd), file = "../Results/counts_total_heatmap.txt", sep = "\t",
            row.names = TRUE, col.names = NA)

res_data <- as.data.frame(assay(ntd))

mean_data <- transform(res_data, Control=(res_data$RC12_Control+res_data$RC14_Control+res_data$RC15_Control)/3)
mean_data <- transform(mean_data, Treated=(res_data$RC17_Treated+res_data$RC18_Treated+res_data$RC19_Treated)/3)
mean_data <- subset(mean_data, select=c(Control,Treated))
dev.off()
pdf("../Results/heatmap_total_mean.pdf")
pheatmap(mean_data, cluster_rows=T, show_rownames=T, show_colnames = T,
         cluster_cols=FALSE,fontsize_row=0.5, clustering_method="ward.D")
## Data visualization
dir.create(file.path(paste0("../Results/glimma-plots")), showWarnings = FALSE)
status <- as.numeric(res$padj < .1)
anno <- data.frame(GeneID=rownames(res))
glMDPlot(res, status=status, counts=counts(des,normalized=TRUE),
         groups=des$Condition, transform=FALSE,
         samples=colnames(des), anno=anno, launch = F, folder = "../Results/glimma-plots")

res05 <- res$padj < 0.05
sum <- summary(res05)
sum
names(sum)[names(sum) == "FALSE"] <- "(DE)[p-adj > 0.05]"
names(sum)[names(sum) == "TRUE"] <- "[p-adj < 0.05]"
names(sum)[names(sum) == "Mode"] <- ""
names(sum)[names(sum) == "logical"] <- "Number of genes"
dev.off()
