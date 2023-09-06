# COMP479-Fall2022

**Information Retrieval and Web Search** course project at Concordia University - assigned by Dr. Sabine Bergler.

## Overview

This assignment has 3 stages: **P1**, **P2**, and **P3**.

#### Built with **Python**.

## Project Stages

### [Project 1 (P1)](/P1)

Text preprocessing with NLTK, proofreading results.

- [Outline](/P1/p1_outline.pdf)
- [Demo](/P1/deliverables/demo.docx)
- [Report](/P1/deliverables/report.docx)

### [Project 2 (P2)](/P2)

Implement a naive indexer, single-term query processing, and lossy dictionary compression (compressed indexer).

- [Outline](/P2/p2_outline.pdf)
- [Demo](/P2/deliverables/demo.pdf)
- [Report](/P2/deliverables/report.pdf)

### [Project 3 (P3)](/P3)

Compile and compute execution time for constructing naive indexer and SPIMI indexer.
Implement Ranked BM25 and Unranked Boolean search engines using SPIMI indexer.

- [Outline](/P3/p3_outline.pdf)
- [Demo](/P3/deliverables/demo.pdf)
- [Report](/P3/deliverables/report.pdf)

## Dataset Used

- **Reuter’s Corpus ["_Reuters-21578_"](./reuters21578_extracted/)**</br>
  (Visit [Original Website](http://www.daviddlewis.com/resources/testcollections/reuters21578/))

## Setup

In this project, [**pypy3**](https://www.pypy.org/) is used as Python3 executable.

#### Install pypy3 on MacOS

`$ brew install pypy3`

#### Install virtualenv

`$ pypy3 -m pip install virtualenv`

#### Create a PyPy virtualenv in the directory pypy-venv

`$ pypy3 -m virtualenv pypy3-env`

#### Start working in the virtual environment

`$ cd ~/pypy3-venv/` </br>
`$ . bin/activate`
