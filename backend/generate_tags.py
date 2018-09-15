#! /usr/bin/env python

import json
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

tags = {}
data = json.load(open("data.json"))
count_vect = CountVectorizer(stop_words='english')


def top_tfidf_feats(row, features, top_n=20):
    topn_ids = np.argsort(row)[::-1][:top_n]
    top_feats = [(features[i], row[i]) for i in topn_ids]
    df = pd.DataFrame(top_feats, columns=['features', 'score'])
    return df

def top_feats_in_doc(X, features, row_id, top_n=25):
    row = np.squeeze(X[row_id].toarray())
    return top_tfidf_feats(row, features, top_n)


for classifiedCompilation in data:
    for article in classifiedCompilation["articles"]:
        joint_paragraph = "\n".join([p["Text"] for p in article["Paragraphs"]])
        if len(joint_paragraph) < 10:
            continue
        X_train_counts = count_vect.fit_transform([joint_paragraph])
        features = count_vect.get_feature_names()
        article_tags = top_feats_in_doc(X_train_counts, features, 0, 5)
        for tag in article_tags.features.tolist():
            if tag not in tags:
                tags[tag] = [article]
            else:
                tags[tag].append(article)

with open("tags.json", "w") as file:
    file.write(json.dumps(tags))      
