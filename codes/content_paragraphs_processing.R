---
title: 'News Article Classification: EDA Report'
author: "Lauren Contard, Archit Datar, Bobby Lumpkin, Yue Li, Haihang Wu"
date: "3/1/2021"
output:
  word_document: default
  pdf_document: default
  html_document: default
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = FALSE)
```

## Introduction

Our project focuses on classification of news articles covering the White House's delivery of news related to covid-19. We begin with a sample of about 8000+ articles from ten mainstream media outlets which were selected using a keyword search. All of these articles are related to covid-19 and the White House in some way; however, not all are focused on White House covid briefings, which is the desired focus of our research. 
1022 of the articles in our sample have been classified by hand into:   
0 = "not related to White House briefings about covid-19" or   
1 = "related to White House briefings about covid-19"   
(Note: these articles were randomly selected from the larger sample, so they should be representative of the full sample of articles.)

Our goal will be to use this sample to build a classifier for the remaining articles. We will do this using the counts of various words that appear in the articles' text; in this exploratory data analysis, we will examine which words may be the most useful as predictors. 

After all the news articles are classified, we will next classify the relavant articles into multiple categories based on the content, such as threat of covid-19, organizational response, self-congratualation, criticizing the government, etc. We will also conduct sentiment analysis to analyze the tone of the news articles. These two steps will not be covered in the exploratory data analysis as our dataset is not clean yet. 

## Text Preprocessing

We began by processing the text of the 1022 classified articles using the "quanteda" package. In this step we:  
-created tokens for all words that appear  
-removed stop words such as "a", "the", etc.  
-stemmed the tokens, e.g. converting "learning" and "learned" to "learn"  
-filtered out words that appear in less than 2.5% and more than 97.5% of articles, as these words may be less useful for prediction


```{r preprocessing, include=FALSE}
####################
#text preprocessing#
####################
#instal packages if you did not use them before. Ignore this step if you have these packages installed. 
#install.packages("quanteda")
#install.packages("readtext")
#install.packages("stringr")

#load the library
library(quanteda)
library(readtext)
library(stringr)

#read in the file using the readtext package
data <- readtext("E:\\osu\\machine_learning\\NewsArticleClassification\\dataset\\content_paragraphs_v1.xlsx", text_field = c("full_text"))

#clean text
data[["text"]] <-  stringr::str_replace_all(data[["text"]],"[^a-zA-Z\\s]", " ")
data[["text"]] <- stringr::str_replace_all(data[["text"]],"[\\s]+", " ")

#build a corpus, that is a bag of words
wh_corpus <- corpus(data)

#explore the corpus texts a little bit. You can skip this step.
kwic(wh_corpus, "trump")

#create tokens (https://www.mzes.uni-mannheim.de/socialsciencedatalab/article/advancing-text-mining/#supervised)
wh_tokens <- tokens(wh_corpus, remove_numbers = TRUE, remove_symbols = TRUE, remove_punct = TRUE, remove_separators = TRUE, include_docvars = TRUE)

#lower case the tokens
wh_tokens <- tokens_tolower(wh_tokens)

#remove stopwords, such as "a" "an" "the" "and" etc
wh_tokens <- tokens_remove(wh_tokens, stopwords("english"))

#stem the tokens (e.g., learning -> learn, learned -> learn)
wh_tokens <- tokens_wordstem(wh_tokens)

#create document-feature matrix
wh_dfm <- dfm(wh_tokens)

#trim the text with dfm_trim. filter out words that appear less than 2.5% and more than 97.5% because these words may be less useful for prediction.
wh_dfm_trim <- dfm_trim(wh_dfm, min_docfreq = 0.025, max_docfreq = 0.975, docfreq_type = "prop")


#The head of the  document-feature matrix is below:


#take a look at the dfm.
head(dfm_sort(wh_dfm_trim, decreasing =TRUE, margin = "both"), n = 10, nf = 10)


#create tf-idf (term-frequency-inverse-ducument-frequency), which is often used as a weighting factor in search for important words to a document in a collection or corpus. (https://en.wikipedia.org/wiki/Tf%E2%80%93idf)
#you can skip this step for now.
titles_tfidf <- dfm_tfidf(wh_dfm_trim)

#convert the dfm to a data frame. We can convert the trimmed dfm or the raw dfm.
wh_dataframe <- convert(wh_dfm, to = "data.frame", docid_field = "doc_id")

#add the document-level variables to the data frame
ready_to_use <- merge(x = wh_dataframe, y = data, by = "doc_id", all = TRUE)


## Exploring the Data

#We now have a data frame with the counts of each tokenized word. 15,267 words were included; the first 50 words are shown here as examples:


# remove the non-binary data from original data set (what existed before pre-processing) ##########columnname in below command should be changed for your interest
drop_cols <- c("para_id", "full.text", "article_id", "word_count", "title", "url", "date.y", "domain","text","threats.impacts","responses.actions",
"self.efficacy","external.efficacy","response.efficacy","public.health","political.evaluation","racial.conflict","international.ralations",
"positive","negative","education","economy","susceptibility")
ready_to_use_NoOriginalData <- ready_to_use[ , !(names(ready_to_use) %in% drop_cols)]

# Check the data dimension
dim(ready_to_use_NoOriginalData)

# See some of the variable names
names(ready_to_use_NoOriginalData)


#We can now compare the distribution of words in the relevant and irrelevant articles. The distribution of the response is:

# Distribution of the response
table(ready_to_use_NoOriginalData$severity)

# Sample proportion 
table(ready_to_use_NoOriginalData$severity) / nrow(ready_to_use)


#Below, we look to see what proportion of "related" articles have a given word in their title, what proportion of "non-related" articles have a word in their title, and the words with largest absolute difference between those two groups. These words might be most useful as features.
##`{r examining predictors}
## proportion of related articles that include words in title ##########columnname in below command should be changed for your interest
related_cases <- ready_to_use_NoOriginalData[ready_to_use_NoOriginalData$neutral== 1, ][,-1]
related_cases <- related_cases[ , which(colnames(related_cases) != 'neutral')]
related_cases_means <- colMeans(related_cases)
related_cases_means[1:10]


#And the same for non-related articles: 


## proportion of non-related articles that include words in title ##########columnname in below command should be changed for your interest
non_related_cases <- ready_to_use_NoOriginalData[ready_to_use_NoOriginalData$neutral== 0, ][,-1]
non_related_cases <- non_related_cases[ , which(colnames(non_related_cases) != 'neutral')]
non_related_cases_means <- colMeans(non_related_cases)
non_related_cases_means[1:10]

## Absolute difference between them
abs_diff_means <- abs(related_cases_means - non_related_cases_means)

## Round and sort the differences
sorted_diffs <- round(sort(abs_diff_means, decreasing = TRUE), digits = 4)
head(sorted_diffs, 10)


## Plotting Data

#The 10 largest differences (related cases - non-related cases) between these frequencies are below:


# difference between related case and non relative case
diff_means <- related_cases_means - non_related_cases_means
#round(sort(diff_means, decreasing = TRUE), digits = 4) ####show the largest and smallest one
head(round(sort(diff_means, decreasing = TRUE), digits = 4), 10)
head(round(sort(diff_means, decreasing = FALSE), digits = 4), 10)


#These are the words that appear to be most strongly associated with related articles. We can visualize the distribution of raw and absolute differences in frequencies over all words:

# visualize the differences ##########columnname in below command should be changed for your interest
plot(sort(diff_means, decreasing = TRUE), xlab = "", ylab = "neutral- Not neutral",
main = "Difference in average frequency")
abline(h=0, lty=2)
plot(sorted_diffs, xlab = "", ylab = "neutral- Not neutral",
main = "Absolute Difference in average frequency")
abline(h=0, lty=2)


#We will consider the top 50 predictors in absolute difference value for the following analysis.
#We will visualize the differences in these predictors with box plots.  

#The 5 variables with the strongest positive difference (i.e., more frequent in "related" than "non-related"):


#We will consider the top 50 predictors in absolute difference value for the following analysis; we draw box plot to visualize it
#top 1-5 variable that has positive effect in related ##########columnname in below command should be changed for your interest
par(mfrow = c(1,5))
boxplot(busi ~ neutral, main = "busi", data = ready_to_use_NoOriginalData)
boxplot(loan  ~ neutral, main = "loan", data = ready_to_use_NoOriginalData)
boxplot(packag ~ neutral, main = "packag", data = ready_to_use_NoOriginalData)
boxplot(peopl ~ neutral, main = "peopl", data = ready_to_use_NoOriginalData)
boxplot(assist ~ neutral, main = "assist", data = ready_to_use_NoOriginalData)


#The 5 variables with the strongest negative differences (i.e., more frequent in "non-related" than "related":


#top 1-5 variable that has negative effect in related; ##########columnname in below command should be changed for your interest
par(mfrow = c(1,5))
boxplot(now ~ neutral, main = "now", data = ready_to_use_NoOriginalData)
boxplot(last ~ neutral, main = "last", data = ready_to_use_NoOriginalData)
boxplot(presid ~ neutral, main = "presid", data = ready_to_use_NoOriginalData)
boxplot(raddatz ~ neutral, main = "raddatz", data = ready_to_use_NoOriginalData)
boxplot(new ~ neutral, main = "new", data = ready_to_use_NoOriginalData)