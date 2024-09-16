# COMP479-P3_Fall-2022

**Information Retrieval and Web Search** course project at Concordia University - assigned by Dr. _Sabine Bergler_.

This assignment has 3 stages: **P1**, **P2**, and **P3**.

This repository is dedicated to stage **P3**.

## Overview

The purpose of this project is to compile and compute execution time for **naïve indexer** and **SPIMI indexer** constructions, and to retrieve and analyze **BM25 ranked results** and **Boolean unranked results** based on given queries.

Given the Reuter’s Corpus [_Reuters-21578_](../reuters21578_extracted/), both naïve indexer and SPIMI indexer extract the raw text of each article from the corpus, tokenize the text for all articles, and compose an inverted index, which is then used for **analysis of ranked and unranked retrieval**.

**IMPORTANT**: The **preprocessing** (i.e. stemming, lowercasing, etc.) was omitted since it was not the necessary topic for this project. However, **stop words** removal is implemented during the input query processing and tokenization, in order to retrieve refined results.

The results for these pipeline steps are specified in the [Demo](./deliverables/demo.pdf) file.

### Outline

- [Outline](p3_outline.pdf)

### Deliverables

- [Report](./deliverables/report.pdf)
- [Demo](./deliverables/demo.pdf)

### Goal

- Compile and measure the execution time required for constructing both the **naive indexer** and the **SPIMI (Single Pass In-Memory Indexing) indexer**.
- Utilize the **SPIMI indexer** to implement two search engines:
  - A **Ranked BM25** search engine, which ranks search results based on relevance using the BM25 algorithm.
  - An **Unranked Boolean** search engine, which performs basic Boolean (AND, OR, NOT) queries.
- Test and analyze your system.
- Discuss how your design decisions influence the results.

## Dataset Used

- **Reuter’s Corpus ["_Reuters-21578_"](../reuters21578_extracted/)**</br>
  (Visit [Original Website](http://www.daviddlewis.com/resources/testcollections/reuters21578/))

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
