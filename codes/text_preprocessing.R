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
library(readxl)

#read in the file using the readtext package
#data <- readtext("data_to_group.csv", text_field = "title")
data <- read_excel("relevant_final_v1.xlsx")

#clean text
data[["text"]] <-  stringr::str_replace_all(data[["full_text"]],"[^a-zA-Z\\s]", " ")
data[["text"]] <- stringr::str_replace_all(data[["full_text"]],"[\\s]+", " ")

#build a corpus, that is a bag of words
titles_corpus <- corpus(data)
summary(titles_corpus)

#explore the corpus texts a little bit. You can skip this step.
kwic(titles_corpus, "trump")

#create tokens (https://www.mzes.uni-mannheim.de/socialsciencedatalab/article/advancing-text-mining/#supervised)
titles_tokens <- tokens(titles_corpus, remove_numbers = TRUE, remove_symbols = TRUE, remove_punct = TRUE, remove_separators = TRUE, include_docvars = TRUE)

#lower case the tokens
titles_tokens <- tokens_tolower(titles_tokens)

#remove stopwords, such as "a" "an" "the" "and" etc
titles_tokens <- tokens_remove(titles_tokens, stopwords("english"))

#stem the tokens (e.g., learning -> learn, learned -> learn)
titles_tokens <- tokens_wordstem(titles_tokens)

#create document-feature matrix
titles_dfm <- dfm(titles_tokens)

#trim the text with dfm_trim. filter out words that appear less than 2.5% and more than 97.5% because these words may be less useful for prediction.
#titles_dfm_trim <- dfm_trim(titles_dfm, min_docfreq = 0.025, max_docfreq = 0.975, docfreq_type = "prop")

#take a look at the dfm.
head(dfm_sort(titles_dfm, decreasing =TRUE, margin = "both"), n = 10, nf = 10)

#create tf-idf (term-frequency-inverse-ducument-frequency), which is often used as a weighting factor in search for important words to a document in a collection or corpus. (https://en.wikipedia.org/wiki/Tf%E2%80%93idf)
#you can skip this step for now.
titles_tfidf <- dfm_tfidf(titles_dfm)

#convert the dfm to a data frame. We can convert the trimmed dfm or the raw dfm.
titles_dataframe <- convert(titles_dfm, to = "data.frame", docid_field = "doc_id")

#add the document-level variables to the data frame
ready_to_use <- merge(x = titles_dataframe, y = data, by = "doc_id", all = TRUE)
