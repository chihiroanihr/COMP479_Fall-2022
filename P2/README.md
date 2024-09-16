# COMP479-P2_Fall-2022

**Information Retrieval and Web Search** course project at Concordia University - assigned by Dr. _Sabine Bergler_.

This assignment has 3 stages: **P1**, **P2**, and **P3**.

This repository is dedicated to stage **P2**.

## Overview

The purpose of this project is to implement a **naïve indexer**, **single-term query search**, and **Compressed Indexer** (a.k.a lossy dictionary compression indexer).

Given the Reuter’s Corpus [_Reuters-21578_](../reuters21578_extracted/), both naïve indexer and compressed indexer extract the raw text of each article from the corpus, **tokenize** the text for all articles, and compose an **inverted index**.

Different results of the inverted index were generated using a naïve indexer and compressed indexer with five reduction processes. The result outputs are specified in the [Demo](./deliverables/demo.pdf) file.

Moreover, single-term query processing is implemented to perform **query search** on both naïve indexer and compressed indexer, using sample queries provided by our professor Ms. _Sabine Bergler_. These result outputs are also specified in the [Demo](./deliverables/demo.pdf) file.

### Outline

- [Outline](p2_outline.pdf)

### Deliverables

- [Report](./deliverables/report.pdf)
- [Demo](./deliverables/demo.pdf)

### Goal

- Implement a **naïve indexer**
- Implement **single-term query processing**
- Implement a **compressed indexer** via lossy dictionary compression techniques
- Compare naïve indexer and compressed indexer

## Dataset Used

- **Reuter’s Corpus ["_Reuters-21578_"](../reuters21578_extracted/)**</br>
  (Visit [Original Website](http://www.daviddlewis.com/resources/testcollections/reuters21578/))

  For **_docID_**, the **_NEWID_** values are used from the Reuters corpus to make data retrieval comparable.

## Programming Language

### Built with **Python**

**Python>=3.8** is used as a programming language for this project due to its compatibility with natural language processing tasks, facilitated by the NLTK package.

## Dependencies

- **BeautifulSoup4**
- **NLTK**

  - _word_tokenize()_
  - **nltk.stem**
    - _PorterStemmer()_
  - nltk.corpus
    - _stopwords_

  (For NLTK package information, refer to [NLTK Packages](https://www.nltk.org/api/nltk.html))

- **PrettyTable**

**BeautifulSoup4** is used for extracting the text data from _**.sgm**_ (dataset) files which are composed of markup languages like HTML and XML.

**NLTK** is used to tokenize, apply Porter Stemmer, and remove stop words from the corpus.

**PrettyTable** is used to make a lossy dictionary compression statistics table.
