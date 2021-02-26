#read in dataset
data <- read.csv("data_to_group.csv", header = T)
#instal packages if you did not use them before. Ignore this step if you have these packages installed. 
install.packages("quanteda")
install.packages("readtext")