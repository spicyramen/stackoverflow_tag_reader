from __future__ import print_function

import re
import matplotlib.pyplot as plt
import nltk
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import MDS
from sklearn.metrics.pairwise import cosine_similarity
from file_reader import get_file_documents

STOP_WORDS = set(stopwords.words("english"))
FILENAME = "/Users/gogasca/Downloads/feedback.csv"
MAX_DF = 0.8
MIN_DF = 0.1
NUM_CLUSTERS = 5


def tokenize_and_stem(document):
    """

    :param document:
    :return:
    """
    # Tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(document) for word in nltk.word_tokenize(sent) if word not in STOP_WORDS]
    filtered_tokens = []
    # Filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)

    stemmer = SnowballStemmer("english")
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(document):
    # Tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(document) for word in nltk.word_tokenize(sent) if word not in STOP_WORDS]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens


def extract_tokens(document_list):
    """

    :param document_list:
    :return:
    """
    totalvocab_stemmed = []
    totalvocab_tokenized = []

    for document in document_list:
        allwords_stemmed = tokenize_and_stem(document)  # for each item in 'document list', tokenize/stem
        totalvocab_stemmed.extend(allwords_stemmed)  # extend the 'totalvocab_stemmed' list
        allwords_tokenized = tokenize_only(document)
        totalvocab_tokenized.extend(allwords_tokenized)

    vocab_frame = pd.DataFrame({'words': totalvocab_tokenized }, index=totalvocab_stemmed)
    print('There are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')
    return vocab_frame


def display_cluster(km, vocab_frame, num_clusters, terms):
    """

    :param km:
    :param vocab_frame:
    :param num_clusters:
    :param terms:
    :return:
    """
    print("Top terms per cluster:")
    # sort cluster centers by proximity to centroid
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    cluster_names = dict()
    idx = 0
    for i in range(num_clusters):
        print("Cluster %d words: " % i, end='')
        for ind in order_centroids[i, :NUM_CLUSTERS]:
            if idx == 0:
                cluster_names[i] = vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore')
            print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'),
                  end=',')
            idx +=1
        print()  # add whitespace
        idx = 0
    return cluster_names

    return


def main():
    """
        Main function
    """
    document_list = get_file_documents(FILENAME)
    vocabulary_frame = extract_tokens(document_list)
    tfidf_vectorizer = TfidfVectorizer(max_df=MAX_DF, max_features=200000,
                                       min_df=MIN_DF, stop_words='english',
                                       use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1, 3))

    tfidf_matrix = tfidf_vectorizer.fit_transform(document_list)  # fit the vectorizer to documents
    terms = tfidf_vectorizer.get_feature_names()
    """
        Dist is defined as 1 - the cosine similarity of each document.
        Cosine similarity is measured against the tf-idf matrix and can be used to generate a measure of similarity
        between each document and the other documents in the corpus (each document among all the documents).
        Subtracting it from 1 provides cosine distance which I will use for plotting on a euclidean
        (2-dimensional) plane.
        Note that with dist it is possible to evaluate the similarity of any two or more documents.
    """
    dist = 1 - cosine_similarity(tfidf_matrix)

    km = KMeans(n_clusters=NUM_CLUSTERS)
    km.fit(tfidf_matrix)
    joblib.dump(km, 'cluster_model.pkl')
    km = joblib.load('cluster_model.pkl')
    clusters = km.labels_.tolist()
    feedback = {'feedback': document_list, 'cluster': clusters}
    frame = pd.DataFrame(feedback, index=[clusters], columns=['cluster'])
    # number of opinions per cluster (clusters from 0 to 4)
    frame['cluster'].value_counts()
    cluster_names = display_cluster(km=km, vocab_frame=vocabulary_frame, num_clusters=NUM_CLUSTERS, terms=terms)
    cluster_colors = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a', 4: '#66a61e'}
#                      5: '#9e1b9d', 6: '#f9f367', 7: '#780a64', 8: '#ec774b', 9: '#4bece1'}

    # Multidimensional scaling
    MDS()
    # convert two components as we're plotting points in a two-dimensional plane
    # "precomputed" because we provide a distance matrix
    # we will also specify `random_state` so the plot is reproducible.
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

    pos = mds.fit_transform(dist)  # shape (n_components, n_samples)

    xs, ys = pos[:, 0], pos[:, 1]
    # create data frame that has the result of the MDS plus the cluster numbers, No title is passed
    df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=None))

    # group by cluster
    groups = df.groupby('label')

    # set up plot
    fig, ax = plt.subplots(figsize=(17, 9))  # set size
    ax.margins(0.05)  # Optional, just adds 5% padding to the autoscaling

    # iterate through groups to layer the plot
    # I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
    for name, group in groups:
        ax.plot(group.x, group.y, marker='o', linestyle='', ms=12,
                label=cluster_names[name], color=cluster_colors[name],
                mec='none')
        ax.set_aspect('auto')
        ax.tick_params( \
            axis='x',  # changes apply to the x-axis
            which='both',  # both major and minor ticks are affected
            bottom='off',  # ticks along the bottom edge are off
            top='off',  # ticks along the top edge are off
            labelbottom='off')
        ax.tick_params( \
            axis='y',  # changes apply to the y-axis
            which='both',  # both major and minor ticks are affected
            left='off',  # ticks along the bottom edge are off
            top='off',  # ticks along the top edge are off
            labelleft='off')

    ax.legend(numpoints=1)  # show legend with only 1 point

    # add label in x,y position with the label as the item title
    for i in range(len(df)):
        ax.text(df.ix[i]['x'], df.ix[i]['y'], '', size=8) # Pass no title, replace '' with object containing titles.

    plt.show()  # show the plot
    plt.close()


if __name__ == '__main__':
    main()
