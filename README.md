# Capstone Project

## Overview
This project analyzes ranking failures in supervised learning-to-rank systems. Rather than focusing on improving overall ranking accuracy, we investigate when and why ranking models place relevant results outside the top-K positions, and how evaluation choices influence the visibility of relevant items. Also, the influence of normalization for early-rank behavior, avoidable failures, and score ties is studied.


## Structure
- data: datasets
- notebooks: analysis notebooks
- src: reusable code

## Status
Project initialized

Phase 1: Exploratory Data Analysis (Completed)
The following steps have been completed:
- Parsed LETOR-formatted data for Fold1
- Verified query and document structure.
- Analyzed label distributions and relevance sparsity
- Identified queries with no relevant documents.
- Examined feature distributions and detected zero-variance features
- Visualized query difficulty, relevance density, and feature behavior

NOTE: Several features were found to have zero variance across all documents. We left them alone for now and will be addressing them later.

*******************************************************
Phase 2: Feature & Query-Level Analysis (Completed)
The following steps have been completed:

- Computed global feature statistics (mean, variance, sparsity)
- Identified zero-variance features across the dataset (f6–f10)
- Analyzed feature scale differences across features
- Examined feature distributions for skewness and heavy tails
- Computed query-level feature variance
- Compared within-query vs between-query variance
- Found that within-query variance dominates, motivating query-aware analysis
- Analyzed relevance sparsity per query
- Categorized queries into:
    Queries with no relevant documents
    Queries with only low-relevance documents
    Queries with at least one highly relevant document
- Quantified feasible vs infeasible queries for ranking evaluation
- Used findings to motivate:
    Conditional evaluation metrics
    Separation of avoidable vs unavoidable failures
- Evaluated normalization strategies conceptually (no normalization applied yet)
- Decided to defer normalization experiments to a controlled later phase

NOTE: No features were normalized or removed in this phase. All conclusions were based on diagnostic analysis only.

**********************************************************

Phase 3: Baseline Ranking System & Failure@K Definition (Completed)

The following steps have been completed:
- Implemented a pointwise baseline ranking model using multinomial Logistic Regression
- Used raw features only (no normalization or feature transformation)
- Explicitly excluded zero-variance features (f6–f10)
- Trained and evaluated using official MQ2007 Fold1 splits
- Used expected relevance score E[y] from class probabilities for ranking
- Defined Failure@K as absence of relevant documents in top-K results
- Evaluated ranking performance using:
    Precision@K
    NDCG@K (graded relevance)
    Failure@K
- Evaluated metrics at K = {1, 3, 5, 10}
- Introduced conditional failure metrics:
    Failure@K | queries with at least one relevant document
    Failure@K | queries with at least one highly relevant document
- Separated avoidable vs unavoidable failures:
    Unavoidable: queries with no relevant documents
    Avoidable: relevant documents exist but not retrieved in top-K
- Verified metric correctness and robustness:
    Guarded against invalid K values
    Handled short queries using min(K, num_docs)
    Validated NDCG implementation against sklearn.metrics.ndcg_score
- Identified tie behavior in ranking scores and recorded tie diagnostics for later analysis
- Stored all baseline predictions, query-level metrics, and aggregates for reproducibility
- Established a stable baseline reference for all subsequent phases

NOTE: No hyperparameter tuning or advanced models were used in this phase. The focus was on interpretability, correctness, and establishing a reliable baseline.


********************************************************

Phase 4: Feature Normalization & Robustness Analysis (Completed)

The following steps have been completed:
- Implemented a controlled normalization framework with three pipelines:
    Raw features (baseline replication)
    Global feature normalization (StandardScaler)
    Per-query feature normalization (z-score within each query)
- Ensured feature consistency across datasets by enforcing presence of all f1–f46 features (missing features filled with 0.0)
- Reproduced Phase 3 raw baseline results exactly within Phase 4 to verify pipeline correctness
- Validated that Phase 4 raw Failure@5 matches Phase 3 Failure@5 up to numerical precision
- Applied all normalization pipelines using a clean, unified pipeline runner API
- Trained the same multinomial Logistic Regression model across all pipelines (no hyperparameter tuning)
- Evaluated models using:
    Precision@K
    NDCG@K (graded relevance)
    Failure@K
- Computed metrics for K belonging to {1, 3, 5, 10}
- Computed conditional failure metrics:
    Failure@K | queries with at least one relevant document
    Failure@K | queries with at least one highly relevant document
- Separated primary relevance (label >= 1) and sensitivity relevance (label == 2) evaluations
- Ran all pipelines on:
    MQ2007 Fold1 (primary dataset)
    MQ2008 Fold1 (generalization check)
- Implemented and computed tie diagnostics, including:
    Number of unique scores in top-K
    Number of tied scores in top-K
    Frequency of ties at the cutoff rank
- Conducted K-sensitivity analysis to examine how Precision@K, NDCG@K, and Conditional Failure@K evolve as K increases
- Performed score flatness analysis to compare score separation (range and standard deviation) between:
    Successful queries
    Avoidable failure queries
- Implemented cross-dataset comparison (MQ2007 vs MQ2008) for Failure@K, Conditional Failure@K, and NDCG@K to assess generalization
- Automatically determined pipeline “winners” based on objective criteria:
    Minimum Conditional Failure@K
    Maximum NDCG@K
- Generated an evidence-based, reproducible Phase 4 summary consolidating:
    Aggregate metrics
    Tie behavior
    Score flatness
    Cross-dataset trends
- Persisted all Phase 4 artifacts, including:
    Query-level metrics
    Aggregate comparisons (primary and sensitivity)
    Diagnostic outputs (tie diagnostics, score flatness, K-sensitivity, cross-dataset comparison)
    Trained models and predictions


**********************************************************
Phase 5
