# COMP479-Fall2022-P1

**Information Retrieval and Web Search** course project at Concordia University - assigned by Dr. _Sabine Bergler_.

This assignment has 3 stages: **P1**, **P2**, and **P3**.

This repository is dedicated to stage **P1**.

## Overview

The purpose of this project is to learn how to **text-preprocess** using **NLTK** library.

Given the Reuter’s Corpus [_Reuters-21578_](../reuters21578_extracted/), this project aims to extract the raw text of each article from the corpus, **tokenize** the text for all articles. Then the project cleans the set of texts by applying **Porter Stemmer** and removing certain **stop words**.

The result of the execution is specified in the [Demo](./deliverables/demo.pdf) file.

### Outline

- [Outline](p1_outline.pdf)

### Deliverables

- [Report](./deliverables/report.pdf)
- [Demo](./deliverables/demo.pdf)

### Goal

- Text preprocessing with **NLTK** (i.e. tokenization, stemming, etc.)
- Proofread results (Ensure the quality of the processed text data.)

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

**BeautifulSoup4** is used for extracting the text data from _**.sgm**_ (dataset) files which are composed of markup languages like HTML and XML.

**NLTK** is used to tokenize, apply Porter Stemmer, and remove stop words from the corpus.
