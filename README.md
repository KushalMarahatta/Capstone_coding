# Capstone Project

## Overview
This project analyzes ranking failures in supervised learning-to-rank systems. Rather than focusing on improving overall ranking accuracy, we investigate when and why ranking models place relevant results outside the top-K positions, and how evaluation choices influence the visibility of relevant items.


## Structure
- data: datasets
- notebooks: analysis notebooks
- src: reusable code

## Status
Project initialized

Phase A: Exploratory Data Analysis (Completed)
The following steps have been completed:
- Parsed LETOR-formatted data for Fold1
- Verified query and document structure.
- Analyzed label distributions and relevance sparsity
- Identified queries with no relevant documents.
- Examined feature distributions and detected zero-variance features
- Visualized query difficulty, relevance density, and feature behavior

NOTE: Several features were found to have zero variance across all documents. We left them alone for now and will be addressing them later.