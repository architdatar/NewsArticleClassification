#%%
import json
import pandas as pd
import os

with open("backup_data/foxnews.json") as f:
    obj_json = json.load(f)
#df  = pd.read_json("foxnews.json")

##Converting to a list. Will come in handy while making dataframe. 
##len(np.diag(pd.read_json("foxnews.json", orient="values")))
# %%
