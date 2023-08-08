Wordview (Work In Progress)
###########################


.. image:: https://img.shields.io/pypi/v/wordview
   :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/wordview
   :alt: PyPI - Python Version

.. image:: https://img.shields.io/pypi/dm/wordview
   :alt: PyPI - Downloads

Wordview is a Python package for Exploratory Data Analysis (EDA) of text.
Wordview's Python API is open-source and available under the `MIT
license <https://en.wikipedia.org/wiki/MIT_License>`__.

|cover|


Usage
######

Install the package via ``pip``:

``pip install wordview``

To explore various features and functionalities, consult the documentation pages. The following sections
present a high-level description of Wordview's features and functionalities. For details, tutorials and worked examples, corresponding 
documentation pages are linked in each section.


Exploratory Data Analysis (EDA)
###############################

Wordview presents many statistics about your data in form of plots and tables allowing you to 
have both a high-level and detailed overview of your data. For instance, which languages
are present in your dataset, how many unique words and unique words are there in your dataset, what percentage 
of them are Adjectives, Nouns or Verbs, what are the most common POS tags, etc. Wordview also provides several statistics for labels in labeled datasets.


Text Analysis
*************
Using this feature, you can have an overview of your text data in terms of various statistics, plots and distribution.
See `text analysis documentation pages <./docs/source/textstats.rst>`__  for usage and examples.


Analysis of Labels
******************
Wordview calculates several statistics for labels in labeled datasets whether they are at document or sequence level.
See `label analysis documentation pages <./docs/source/labels.rst>`__ for usage and examples.


Extraction & Analysis of Multiword Expressions
**********************************************
Multiword Expressions (MWEs) are phrases that can be treated as a single
semantic unit. E.g. *swimming pool* and *climate change*. MWEs have
application in different areas including: parsing, language models,
language generation, terminology extraction, and topic models. Wordview can extract different types of MWEs from text.
See `MWEs documentation page <./docs/source/mwes.rst>`__ for usage and examples.


Bias Analysis
**************
In the rapidly evolving realm of Natural Language Processing (NLP), downstream models are as unbiased and fair as the data on which they are trained.
Wordview Bias Analysis module is designed to assist in the rigorous task of ensuring that underlying training datasets are devoid of explicit negative biases related to categories such as gender, race, and religion.
By identifying and rectifying these biases, Wordview attempts to pave the way for the creation of more inclusive, fair, and unbiased NLP applications, leading to better user experiences and more equitable technology.
See the `bias analysis documentation page <./docs/source/bias.rst>`__ for usage and examples.


Analysis of Anomalies and Outliers
**********************************
Anomalies and outliers have wide applications in Machine Learning. While in
some cases, you can capture them and remove them from the data to improve the
performance of a downstream ML model, in other cases, they become the data points
of interest where we endeavor to find them in order to shed light into our data.

Wordview offers several anomaly and outlier detection functions.
See `anomalies documentation page <./docs/source/anomalies.rst>`__ for usage and examples.




Cluster Analysis
****************
Clustering can be used to identify different groups of documents with similar information, in an unsupervised fashion.
Despite it's ability to provide valuable insights into your data, you do not need labeled data for clustering. See
`wordview`'s `clustering documentation page <./docs/source/clustering.rst>`__ for usage and examples.


Utilities
#########

Wordview offers a number of utility functions that you can use for common pre and post processing tasks in NLP. 
See `utilities documentation page <./docs/source/utilities.rst>`__ for usage and examples.

Contributing
############

Thank you for contributing to wordview! We and the users of this repo
appreciate your efforts! You can visit the `contributing page <CONTRIBUTING.rst>`__ for detailed instructions about how you can contribute to Wordview.

.. |cover| image:: docs/figs/cover.png
