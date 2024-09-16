# COMP479_Fall2022

**Information Retrieval and Web Search** course project at Concordia University - professor by Dr. _Sabine Bergler_.

## Overview

This assignment has 3 stages: **P1**, **P2**, and **P3**.

### Built with **Python**

**Python>=3.8** is used as a programming language for this project due to its compatibility with natural language processing tasks, facilitated by the NLTK package.

## [Project 1 (P1)](/P1): Text Preprocessing and Proofreading

### Key Tasks

- Utilize **NLTK** for text preprocessing, which involves tasks like tokenization and stemming.
- Proofread and ensure the quality of the processed text data.

### Resources

- [Outline](/P1/p1_outline.pdf)
- [Demo](/P1/deliverables/demo.pdf)
- [Report](/P1/deliverables/report.pdf)

## [Project 2 (P2)](/P2): Indexing and Query Processing

### Key Tasks

- Implement a **naive indexer** for indexing documents.
- Develop a mechanism for processing single-term queries.
- Apply lossy dictionary compression techniques to create a **compressed indexer**.

### Resources

- [Outline](/P2/p2_outline.pdf)
- [Demo](/P2/deliverables/demo.pdf)
- [Report](/P2/deliverables/report.pdf)

## [Project 3 (P3)](/P3): Performance Analysis and Search Engine Implementation

### Key Tasks

- Compile and measure the execution time required for constructing both the **naive indexer** and the **SPIMI (Single Pass In-Memory Indexing) indexer**.
- Utilize the **SPIMI indexer** to implement two search engines:
  - A **Ranked BM25** search engine, which ranks search results based on relevance using the BM25 algorithm.
  - An **Unranked Boolean** search engine, which performs basic Boolean (AND, OR, NOT) queries.

### Resources
- [Outline](/P3/p3_outline.pdf)
- [Demo](/P3/deliverables/demo.pdf)
- [Report](/P3/deliverables/report.pdf)

## Dataset Used

- **Reuter’s Corpus ["_Reuters-21578_"](./reuters21578_extracted/)**</br>
  (Visit [Original Website](http://www.daviddlewis.com/resources/testcollections/reuters21578/))

## Setup

In this project, [**pypy3**](https://www.pypy.org/) is used as Python3 executable. 

[**Pypy3**](https://www.pypy.org/) serves as a substitute for the native Python3 interpreter due to its superior runtime performance. Given that these projects involve processing an extensive volume of large files through iterative operations, opting for pypy3 as an alternative interpreter was a highly efficient decision.

#### Install pypy3

`$ brew install pypy3`

#### Install virtualenv

`$ pypy3 -m pip install virtualenv`

#### Create a PyPy virtualenv in the directory pypy-venv

`$ pypy3 -m virtualenv pypy3-env`

#### Start working in the virtual environment

`$ cd ~/pypy3-venv/` then `$ . bin/activate`
