#%%
"""Combine article data from json file into a single dataframe.
"""
import json
import pandas as pd

combined_df =  pd.DataFrame() #columns=["Index_str", "Article_text"])

df = pd.read_csv("~/repo/StatMachLearn/NewsArticleClassification/data_to_group_copy.csv", header=0)
domain_list =  list(set(df['domain'].values))

domain_list.remove("wsj.com")

for domain in domain_list:
    print(domain)
    with open(f"backup_data/{domain.rsplit('.', 1)[0]}.json") as f:
        obj_json = json.load(f)
        for article_dict in obj_json:
            print(article_dict.keys())
            try:
                #combined_df.append({"Index_str": article_dict[0], "Article_text": article_dict[1] })
                #combined_df = combined_df.append(article_dict, ignore_index=True)
                new_df = pd.DataFrame.from_dict(article_dict, orient="index")
                combined_df = combined_df.append(new_df)
            except Exception as e:
                print(e)
                continue

combined_df.columns = ["Article_text"]
combined_df["Index_str"] = combined_df.index
combined_df["Index"] = combined_df["Index_str"].apply(lambda x: int(x))

df_with_article_data = df.merge(combined_df[["Index", "Article_text"]], left_on="id", right_on="Index")
df_with_article_data.to_excel("dataframe_with_article_data.xlsx", index=False)
# %%
