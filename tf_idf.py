from sklearn.feature_extraction.text import TfidfVectorizer

class tf_idf():
    """This class is in charge of performing TF/IDF for a corpus"""
    def __init__(self):
        self._corpus = None

    @property
    def corpus(self):
        """I'm the answer Body roperty."""
        return self._corpus

    @corpus.setter
    def corpus(self, corpus):
        self._corpus = corpus

    def tf_idf(self, corpus):
        """

        :param corpus:
        :return:
        """
        vectorizer = TfidfVectorizer(min_df=1)
        X = vectorizer.fit_transform(corpus)
        idf = vectorizer.idf_
        return dict(zip(vectorizer.get_feature_names(), idf))

    def print_tfids(self):
        """

        :return:
        """

        tf_idfs = self.tf_idf(self.corpus)
        for word in sorted(tf_idfs, key=tf_idfs.get, reverse=True):
            print word, tf_idfs[word],
