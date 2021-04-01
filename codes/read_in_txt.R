library(httr)
library(jsonlite)
library(devtools)
library(urltools)
library(readr)
library(dplyr)
library(tidyr)
library(zoo)
library(forcats)
library(scales)
library(stringr)
library(gridExtra)

setwd("C:/Users/li.7232/OneDrive - The Ohio State University/NewsArticleClassification/dataset/full_text_v1")

# first get a list of the file names 
daily_filenames <- list.files("C:/Users/li.7232/OneDrive - The Ohio State University/NewsArticleClassification/dataset/full_text_v1")

# loop over the file names
data <- c()
for(i in 1:length(daily_filenames)){
  this_data <- c()
  if (!file.size(daily_filenames[i]) == 0) {
  # read in each file
  full_text <- readLines(paste0("C:/Users/li.7232/OneDrive - The Ohio State University/NewsArticleClassification/dataset/full_text_v1/", daily_filenames[i]))
  # make the article id = text file id
  this_data <- data.frame(full_text = full_text)
  this_data$article_id <- parse_number(daily_filenames[i])
  # count the word frequency and generate a brief file
  this_data$word_count <- lengths(gregexpr("\\W+", this_data$full_text)) + 1
  # if it is the first file, make it the object data
  if(i==1) data <- this_data
  # if it is not the first file, append the new data file to the old one
  if (i > 1) data <- bind_rows(data, this_data)
  # check on progress -- works very fast on my laptop!
  print(i)
  }
}

#remove the empty rows
data <- data[!(data$full_text == ""), ]

write.csv(data, "full_paragraph_v1.csv")