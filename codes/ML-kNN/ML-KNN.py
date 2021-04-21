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

####### PCA to understand if there are features we can drop. 
from sklearn.decomposition import PCA
#pca = PCA(n_components=2)
pca = PCA(n_components=len(feature_list))
pca.fit(df[feature_list])
print(pca.explained_variance_ratio_)

PC_values = np.arange(pca.n_components_) + 1
plt.plot(PC_values, pca.explained_variance_ratio_, 'ro-', linewidth=2)

# component_df = pd.DataFrame(pca.components_[:5],columns=df[feature_list].columns, index = ['PC-1','PC-2', 'PC-3', 'PC-4' 
#                                                                                                     ])
# display(component_df.T)
# pca.score_samples(df[feature_list]).shape
# X_transformed = pca.transform(df[feature_list])

# df["trans_X"] = X_transformed[:, 0]
# df["trans_Y"] = X_transformed[:, 1]
# df["trans_Z"] = X_transformed[:, 2]


"""
###################
# X_train = np.random.random(size=(10,5))
# y_train = np.random.randint(0, 2, size=(10,2))
X_train = df[feature_list[:5]].values
y_train = df[label_list].values


classifier = MLkNN(k=3)

classifier.fit(X_train, y_train)

y_test = classifier.predict(np.random.random(size=(2,5)))

y_test_array = y_test.toarray()
"""

#Questions: 
#1. How to shortlist variables? Use all variables. Then, PCA, find features, etc. 
#2. How to test accuracy? Hamming loss
#3. How many can we use? 
#4. Cross-validation with number of neighbors. 
#5. ML-kNN is feature space with larger dimensions than #training points? 
# %%
