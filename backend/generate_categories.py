#! /usr/bin/env python

#
# Unsupervised categorize paragraphs for every article
#
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pdb

vect = TfidfVectorizer(stop_words='english', max_df=0.50, min_df=2)
data = json.load(open("data.json"))

paragraphs = []
articles = []

# Read json
for classifiedCompilation in data:
    for article in classifiedCompilation["articles"]:
        articles.append(article)
        joint_paragraph = " ".join([p["Text"] for p in article["Paragraphs"]])
        paragraphs.append(joint_paragraph)

X = vect.fit_transform(paragraphs)
features = vect.get_feature_names()

#X_dense = X.todense()
# coords = PCA(n_components=2).fit_transform(X_dense)
# plt.scatter(coords[:, 0], coords[:, 1], c='m')
# plt.show()

n_clusters = 10
clf = KMeans(n_clusters=n_clusters, max_iter=100, init='k-means++', n_init=1)
labels = clf.fit_predict(X)

i = 0
for classifiedCompilation in data:
    for article in classifiedCompilation["articles"]:
        article["category"] = int(labels[i])
        i += 1

with open("data_with_categories2.json", "w") as file:
    file.write(json.dumps(data, indent=4))

pdb.set_trace()
def top_tfidf_feats(row, features, top_n=20):
    topn_ids = np.argsort(row)[::-1][:top_n]
    top_feats = [(features[i], row[i]) for i in topn_ids]
    df = pd.DataFrame(top_feats, columns=['features', 'score'])
    return df

def top_feats_in_doc(X, features, row_id, top_n=25):
    row = np.squeeze(X[row_id].toarray())
    return top_tfidf_feats(row, features, top_n)


def top_mean_feats(X, features, grp_ids=None, min_tfidf=0.1, top_n=25):
    if grp_ids:
        D = X[grp_ids].toarray()
    else:
        D = X.toarray()
    D[D < min_tfidf] = 0
    tfidf_means = np.mean(D, axis=0)
    return top_tfidf_feats(tfidf_means, features, top_n)

def top_feats_per_cluster(X, y, features, min_tfidf=0.1, top_n=25):
    dfs = []
    labels = np.unique(y)
    for label in labels:
        ids = np.where(y==label) 
        feats_df = top_mean_feats(X, features, ids,    min_tfidf=min_tfidf, top_n=top_n)
        feats_df.label = label
        dfs.append(feats_df)
    return dfs

tags = top_feats_per_cluster(X, labels, features, 0.1, 10)
for i, tag_cat in enumerate(tags):
    print("Categories {}: {}".format(i, tag_cat))

i = 0
for classifiedCompilation in data:
    for article in classifiedCompilation["articles"]:
        category = labels[i]
        article["category"] = int(category)
        i =+ 1


converted_tags = [t.features.tolist() for t in tags]
with open("categories.json", "w") as file:
    file.write(json.dumps(converted_tags, indent=4))