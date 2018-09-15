import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import numpy as np
import copy

VECT = TfidfVectorizer(stop_words='english', max_df=0.50, min_df=2)
COUNT_VECT = CountVectorizer(stop_words='english')


def predict_tags_old(data, paragraphs, n_clusters=100):
    X = VECT.fit_transform(paragraphs)
    features = VECT.get_feature_names()
    kmeans = KMeans(n_clusters=n_clusters, max_iter=100, init='k-means++', n_init=1)
    labels = kmeans.fit_predict(X)
    # Get 5 tags
    tags = top_feats_per_cluster(X, labels, features, 0.1, 5)
    return labels[-1], get_categorized_data(data, labels), [t.features.tolist() for t in tags][labels[-1]]

def predict_tags(data, tags, sentence):
    X = COUNT_VECT.fit_transform([sentence])
    features = COUNT_VECT.get_feature_names()
    tags_to_search = top_feats_in_doc(X, features, 0, 5).features.tolist()
    articles = []
    for tag in tags_to_search:
        article = tags.get(tag, None)
        if not article:
            continue
        articles.extend(article)
        if len(articles) > 5:
            articles = articles[0:5]
            break

    result = []
    class_id = [a["ClassifiedCompilation"][0] for a in articles]
    full_id = [a["FullId"] for a in articles]
    for cc in copy.deepcopy(data):
        if cc["CCNr"] in class_id:
            cc["articles"] = [a for a in cc["articles"]  if a["FullId"] in full_id]
            result.append(cc)
    return (result, tags_to_search)


def get_categorized_data(data, labels):
    i = 0
    for classifiedCompilation in data:
        for article in classifiedCompilation["articles"]:
            article["category"] = int(labels[i])
            i += 1
    return data


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

