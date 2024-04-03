
library(ggplot2)
library(qqplotr)
library(pastecs)
theme_set(theme_minimal())

setwd("/Users/feliperodriguez/OneDrive - Bellevue University/Github/dsc520/")

acs_data <- read.csv("data/acs-14-1yr-s0201.csv")

colnames(acs_data)
lapply(acs_data, class)


str(acs_data)

nrow(acs_data)

ncol(acs_data)

acs_hist <- ggplot(acs_data, aes(HSDegree)) + 
  ggtitle('Count of High School Degrees') + 
  xlab('High School Degree Percentages') + 
  ylab('Density of Occurances') + 
  geom_histogram(aes(y=..density..), bins = 25)
acs_hist

acs_hist + geom_density()

acs_prob_plot <- ggplot(mapping = aes(sample = acs_data$HSDegree)) + 
  stat_qq_point(size = 1,color = "blue", xlim=c(50,125), ylim=c(50,125)) + 
  ggtitle("High School Degree Plot") + 
  xlab("High School Degree %") + ylab("Frequency")
acs_prob_plot

stats <- stat.desc(acs_data$HSDegree, norm=TRUE)
stats
str(stats)

HSDegree_mean <- mean(acs_data$HSDegree)
HSDegree_sd <- sd(acs_data$HSDegree)
HSDegree_zscore <- ((acs_data$HSDegree - hsdegree_mean)/HSDegree_sd)
matrix_zscore <- matrix(HSDegree_zscore, nrow=136)
colnames(matrix_zscore) <- c("z_score")
rownames(matrix_zscore) <- c(acs_data$Id)
head(matrix_zscore)

##Data Type Dictionary

Id - Data Type: character Definition: Unique identifier for the record
Id2 - Data Type: integer Definition: Last 5 digits of Id
Geography - Data Type: character Definition: County and State for the record
POPGROUPID - Data Type: integer Definition: Unique Identifier for population group
POPGROUP.display.label - Data Type: character Definition: Population group label
HSDegree - Data Type: numeric Definition: Percentage amount of population with High School Degree
BachDegree - Data Type: numeric Definition: Percentage amount of population with Bachelors Degree

