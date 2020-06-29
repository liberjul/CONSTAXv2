###############################################
#       Taxonomy Assignment Comparison        #
#               Gian MN Benucci               #
#             benucci[at]msu.edu              #
###############################################

if(!require(ggplot2)){
  install.packages("ggplot2")
  library(ggplot2)
}

args <- commandArgs(trailingOnly=TRUE)
output_dir <- args[1]
blast <- as.logical(args[2])
format <- args[3]

# comb_tax = read.table(paste(output_dir, "combined_taxonomy.txt", sep=""), header=TRUE, row.names=1, sep="\t")
comb_tax = read.table(paste(output_dir, "combined_taxonomy.txt", sep=""), sep="\t")
head(comb_tax)
system.time(comb_tax[comb_tax==''|comb_tax==' ']<-NA)

sapply(comb_tax, function(x) sum(is.na(x))) -> unassigned_comb_tax
comb_tax_df <- as.data.frame(unassigned_comb_tax)
if (format == "UNITE"){
  if (blast){
    comb_tax_df$Classifier <- rep(c("RDP", "BLAST", "SINTAX", "COMBINED"), 7)

    comb_tax_df$Rank <- row.names(comb_tax_df)
    comb_tax_df$Assigned <- sqrt((comb_tax_df$unassigned_comb_tax -nrow(comb_tax))^2)
    comb_tax_df

    comb_tax_df$Classifier <- factor(comb_tax_df$Classifier, levels = c("RDP","BLAST","SINTAX","COMBINED"))
  } else {
    comb_tax_df$Classifier <- rep(c("RDP", "SINTAX", "UTAX", "COMBINED"), 7)

    comb_tax_df$Rank <- row.names(comb_tax_df)
    comb_tax_df$Assigned <- sqrt((comb_tax_df$unassigned_comb_tax -nrow(comb_tax))^2)
    comb_tax_df

    comb_tax_df$Classifier <- factor(comb_tax_df$Classifier, levels = c("RDP","UTAX","SINTAX","COMBINED"))
  }
} else {
  rank_count <- (dim(comb_tax)[1]-1)/3
  if (blast){
    comb_tax_df$Classifier <- rep(c("RDP", "BLAST", "SINTAX", "COMBINED"), rank_count)

    comb_tax_df$Rank <- row.names(comb_tax_df)
    comb_tax_df$Assigned <- sqrt((comb_tax_df$unassigned_comb_tax -nrow(comb_tax))^2)
    comb_tax_df

    comb_tax_df$Classifier <- factor(comb_tax_df$Classifier, levels = c("RDP","BLAST","SINTAX","COMBINED"))
  } else {
    comb_tax_df$Classifier <- rep(c("RDP", "SINTAX", "UTAX", "COMBINED"), rank_count)

    comb_tax_df$Rank <- row.names(comb_tax_df)
    comb_tax_df$Assigned <- sqrt((comb_tax_df$unassigned_comb_tax -nrow(comb_tax))^2)
    comb_tax_df

    comb_tax_df$Classifier <- factor(comb_tax_df$Classifier, levels = c("RDP","UTAX","SINTAX","COMBINED"))
  }
}


pdf(paste(output_dir, "TaxonomicAssignmentComparison_plot.pdf", sep=""))
ggplot(comb_tax_df, aes(x = Rank, y = Assigned, fill= Classifier)) +
  geom_bar(stat = "identity") +
  scale_x_discrete(limits=comb_tax_df$Rank) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1),
        panel.grid=element_blank(),
        panel.background=element_blank()) +
  #scale_fill_manual(values=mycols) +
  ggtitle("Taxonomy Assignments Comparison") +
  labs(x="Taxonomic Ranks", y="Number of classified OTUs") +
  theme(axis.text.x = element_text(vjust=0.5, size=8)) +
  theme(axis.text.y = element_text(hjust=0.5, size=8)) +
  theme(plot.title = element_text(size = 15, face = "bold", hjust = 0.5))
dev.off()
