# coding=utf-8
import re

import nltk
from bs4 import BeautifulSoup


class Formatter(object):
    def __init__(self):
        self._remove_tags = ["script", "style"]
        self._text = None
        self._hrefs = []
        self._tokens = []

    @property
    def hrefs(self):
        """
        Return a single List of href
        :return:
        """
        return self._hrefs

    @hrefs.setter
    def hrefs(self, hrefs):
        self._hrefs = hrefs

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        """

        :param text:
        :return:
        """
        self._text = text

    def extract_urls(self, text):
        """

        :param text:
        :return:
        """
        a_hrefs = []

        for element in text:
            soup = BeautifulSoup(element, "lxml")
            a_hrefs.append(soup.find_all("a", href=True))
            # Scripts and styles
        self._hrefs = [x for b in a_hrefs for x in b]
        return self._hrefs

    def beautify(self, text):
        """

        :param text:
        :return:
        """
        text_elements = []
        if text:
            soup = BeautifulSoup(text, "lxml")
            # Scripts and styles
            for script in soup(self._remove_tags):
                script.extract()
            text = soup.get_text()
            text_elements.append(text)

            return ' '.join(text_elements)

    def tokenize(self):
        """
        # Tokenize by sentence, then by word to ensure that punctuation is caught as it's own token

        """
        tokens = [word.lower() for sent in nltk.sent_tokenize(self.text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)

        self._tokens = filtered_tokens


"""
f = Formatter()
f.text = [
    u'<br /><p>First of all, I\'m trying AMP for the first time and I don\'t have enough knowledge about it. And I installed <a href="https://github.com/Automattic/amp-wp" rel="nofollow">AMP for WordPress</a> plugin, and it seems everything is setup successfully. The articles on my site are now having a link tag with the value of <code>amphtml</code> for <code>rel</code> attribute.</p>\n\n<pre><code>&lt;link rel="amphtml" href="http://example.com/link-to-amp-version-of-article/amp/"&gt;\n</code></pre>\n\n<p>And a canonical url on the amp version of articles</p>\n\n<pre><code>&lt;link rel="canonical" href="http://example.com/link-to-original-version-of-article/"&gt;\n</code></pre>\n\n<p>Now visiting that amp version of post url works. But, when I search on google for any of my site\'s article, clicking them doesn\'t take me to the AMP version of url. Wasn\'t that should be? (<em>please enlighten me if I\'m wrong</em>). <a href="https://www.ampproject.org/docs/guides/validate.html" rel="nofollow">Validation of amp</a> urls is giving no errors. What am I missing?</p>\n',
    u'<p>As today, Google is using AMPs for the AMP-based news carousel in Mobile Search and Google News:\n<a href="https://productforums.google.com/forum/#!msg/webmasters/gECaJ0KGxgQ/c3NhRn41CQAJ" rel="nofollow">https://productforums.google.com/forum/#!msg/webmasters/gECaJ0KGxgQ/c3NhRn41CQAJ</a></p>\n\n<p>Other platforms are also displaying AMP versions of news articles when available:\n<a href="https://blog.twitter.com/2016/explore-links-in-moments-1" rel="nofollow">https://blog.twitter.com/2016/explore-links-in-moments-1</a></p>\n']

print f.text
print '****'
print f.beautify(f.text)
print '****'
print f.extract_urls(f.text)
"""
