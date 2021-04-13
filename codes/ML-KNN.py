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
#df = pd.read_t

X_train = np.random.random(size=(10,5))
y_train = np.random.randint(0, 2, size=(10,2))

classifier = MLkNN(k=3)

classifier.fit(X_train, y_train)

y_test = classifier.predict(np.random.random(size=(2,5)))

y_test_array = y_test.toarray()
# %%
