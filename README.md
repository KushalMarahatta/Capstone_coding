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
Phase 5: Query-level Failure Taxonomy and Diagnostic ANalysis (completed)

- Shifted project focus from metric improvement to structured failure diagnosis

- Defined avoidable failures as:
    Queries with at least one relevant document (num_relevant_1 > 0)
    AND Failure@5_primary == True

- Implemented a multi-label query-level failure taxonomy including:
    Flat-score failures (low score separation in top-10)
    Tie-driven failures (ties at cutoff rank)
    Weak-signal failures (relevant documents ranked below K)
    Weak-signal sensitivity failures (highly relevant documents ranked below K)
    Relevance-sparse failures (only one relevant document in query)

- Established primary failure label priority ordering:
    tie_driven > relevance_sparse > weak_signal_primary > flat_score > other

- Ensured categories remain multi-label (queries may belong to multiple failure types)

- Computed score separation diagnostics:
    score_range_top10
    score_std_top10

- Determined flat-score threshold using data-driven procedure:
    Collected score_std_top10 from avoidable failures
    Selected 25th percentile threshold
    Conducted threshold sensitivity sweep to validate robustness

- Verified that conclusions do not depend heavily on threshold choice

- Generated query-level failure profiles for:
    MQ2007 Fold1
    MQ2008 Fold1

- Computed failure category distributions for each pipeline:
    Raw
    Global normalization
    Per-query normalization

- Performed cross-pipeline overlap analysis to identify:
    Persistent failures (fail in all pipelines)
    Rescued queries (raw fail -> normalized success)
    Hurt queries (raw success -> normalized fail)

- Quantified normalization tradeoffs (rescues vs hurts)

- Selected representative case studies for:
    Flat-score failure
    Relevance-sparse failure
    Weak-signal failure
    Persistent failure
    Normalization tradeoff (hurt case)

- Generated detailed ranking diagnostics for selected queries, including:
    Top-10 ranked documents
    Score values
    Relevance markers
    Rank recomputation from scores

- Preserved tie diagnostics for interpretability and robustness



************************************************************

Phase 6: Stronger LTR Models + Replication of Baseline Comparisons (Completed)


The following steps have been completed:

- Expanded the modeling layer from a single pointwise baseline to three model families:
  - Pointwise (baseline logistic regression reference)
  - Pairwise (rank-learning objective)
  - LightGBM ranker (tree-based learning-to-rank)

- Standardized evaluation across all model × pipeline combinations:
  - Models: {pointwise, pairwise, lightgbm}
  - Pipelines: {raw, global, per_query}
  - Datasets: {MQ2007 Fold1, MQ2008 Fold1}

- Enforced strict comparability rules:
  - Same Fold1 split usage across MQ2007 and MQ2008 (train/test kept consistent)
  - Same evaluation metrics and Failure@K definition as earlier phases
  - No "hidden" changes to thresholds, relevance definitions, or K values across configs

- Trained each model under each preprocessing pipeline:
  - Raw: no feature scaling
  - Global normalization: StandardScaler applied globally
  - Per-query normalization: z-score normalization within each query group

- Evaluated all configs using the same query-level metric outputs required for later phases:
  - NDCG@5 (graded relevance)
  - P@5_primary
  - Failure@5_primary
  - Plus required per-query metadata to support filtering and interpretability:
    - num_relevant_1 (count of label ≥ 1 docs per query)
    - (and any additional query diagnostics persisted from earlier phases where applicable)

- Preserved the primary vs sensitivity evaluation convention:
  - Primary relevance: label ≥ 1
  - Sensitivity relevance: label == 2
  - Saved sensitivity aggregates separately (when produced in Phase 6) to remain consistent with Phase 3–5 conventions.

- Implemented robust metric safeguards carried forward from Phase 3–5:
  - Metric definitions handle short queries using min(k, n_docs)
  - relevance_threshold is validated explicitly (only valid values allowed)
  - Tie-handling policy is made explicit and diagnostics are preserved where relevant

- Produced Phase 6 artifacts in a “Phase 7-ready” format (no recomputation needed later):
  - Query-level metrics are exported per config and dataset
  - Outputs are deterministic and reproducible (stable naming + consistent schema)
