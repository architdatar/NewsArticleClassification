"""
In this file, we use the ML-KNN model to predict and analyze data for the news articles. 
"""

#%%
import numpy as np 
import scipy
import matplotlib.pyplot as plt
import pandas as pd

from skmultilearn.adapt import MLkNN

#import data
df = pd.read_csv("../dataset/content_paragraphs_ready.csv", header=0)

label_list = ["threats/impacts", "responses/actions", "severity", 
        "susceptibility", "self-efficacy", "external-efficacy", "response efficacy", 
        "public health", "economy", "education", "political evaluation", "racial conflict", 
        "international ralations/foreign policies", "positive", "negative"]
feature_list = list(df.columns[25:])

df = df[["para_id"] + label_list + feature_list]


# X_train = np.random.random(size=(10,5))
# y_train = np.random.randint(0, 2, size=(10,2))
X_train = df[feature_list[:5]].values
y_train = df[label_list].values


classifier = MLkNN(k=3)

classifier.fit(X_train, y_train)

y_test = classifier.predict(np.random.random(size=(2,5)))

y_test_array = y_test.toarray()


#Questions: 
#1. How to shortlist variables? 
#2. How to test accuracy?
#3. How many can we use? 
#4. Cross-validation with number of neighbors. 

# %%
