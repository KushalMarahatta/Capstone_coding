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





  *****************************************************************************************************


  Phase 7: Statistical Significance & Comparative Inference (Completed)

  The following steps have been completed:

- Established a formal statistical testing framework to evaluate whether performance differences vs baseline are statistically significant

- Used pointwise_raw as the explicit baseline reference for all comparisons

- Conducted paired statistical tests for performance metrics:
    Wilcoxon signed-rank test for NDCG@5 differences
    Wilcoxon signed-rank test for Precision@5 differences
    McNemar’s test for Failure@5 paired binary outcomes

- Performed analysis separately for:
    MQ2007 Fold1
    MQ2008 Fold1 (generalization dataset)

- Computed effect sizes alongside statistical tests:
    Cliff’s delta for NDCG@5 and P@5
    Risk difference for Failure@5

- Calculated 95% confidence intervals:
    Bootstrap CI for median differences (NDCG@5, P@5)
    Confidence intervals for failure risk differences

- Applied Benjamini–Hochberg False Discovery Rate (FDR) correction across multiple comparisons within each dataset

- Explicitly separated:
    Raw p-values (pval_raw)
    FDR-adjusted q-values (qval_fdr)

- Introduced effect size thresholds to avoid overclaiming statistical significance:
    |Cliff’s δ| ≥ EFFECT_SMALL for NDCG and P@5
    |risk_diff| ≥ FAILURE_EFFECT_SMALL for Failure@5

- Defined a result as “supported” only if:
    qval_fdr < FDR_ALPHA
    AND effect size ≥ predefined threshold

- Generated deterministic, sorted CSV artifacts for reproducibility:
    phase7_stats_ndcg_vs_baseline.csv
    phase7_stats_failure_vs_baseline.csv
    phase7_stats_p5_vs_baseline.csv

- Built structured JSON summary (phase7_summary.json) containing:
    Best-performing configuration per dataset
    Number of FDR-significant improvements per metric
    Failure reduction summaries
    Warning logs

- Generated visual diagnostics for MQ2007:
    Bar plots of median NDCG@5 difference with 95% CI
    Bar plots of Failure@5 risk difference with 95% CI

- Implemented generalization diagnostics across datasets:
    Detected direction reversals (sign flips)
    Identified configurations significant only in MQ2007 or only in MQ2008
    Flagged potential generalization inconsistencies


NOTE: Phase 7 did not introduce new models or feature engineering. The focus was on rigorous statistical validation of previously observed performance differences, controlling for multiple comparisons and enforcing effect-size-aware interpretation.




*********************************************************************************************************************************


************************************************************

Phase 8: Structural Root-Cause Analysis of Persistent Failures (Completed)

The following steps have been completed:

- Transitioned from performance-level evaluation (Phase 7) to structural-level diagnosis of persistent ranking failures

- Defined three disjoint query groups using Phase 6 artifacts (MQ2007 Fold1, baseline reference = pointwise_raw_2007):
  - Persistent: queries failing in all 9 model x pipeline configs
  - Non-persistent: queries failing in >=1 but not all configs
  - Successful: queries never failing

- Enforced strict analysis-only constraints:
  - No retraining of models
  - No regeneration of predictions
  - No threshold or relevance-definition changes
  - All analysis based exclusively on Phase 6 query-level artifacts + raw MQ2007 test features

- Constructed structural diagnostics across multiple dimensions:
  - Relevance sparsity (num_relevant_1, pct_num_rel_eq_1)
  - Score separability (best relevant score - rank-5 score gap)
  - Top-10 score dispersion (score_std_top10)
  - Composite hardness index combining sparsity and dispersion
  - Feature-level signal comparison (within-query variance and zero-percentage)

- Implemented safe alignment checks between raw test features and prediction artifacts to prevent feature–score misalignment

- Re-loaded raw MQ2007 Fold1 test features (f1-f46):
  - Ensured missing feature columns are explicitly added as 0.0
  - Dropped known zero-variance features identified in Phase 2
  - Preserved deterministic feature ordering

- Computed structural group summaries using the baseline configuration only to maintain interpretability consistency across phases

- Developed multiple visualization diagnostics for structural interpretation:
  - Relevance distribution comparisons
  - Score gap distributions
  - Hardness strip plots and density diagnostics
  - Feature variance comparison tables

- Established a formal structural significance testing framework:
  - Mann–Whitney U tests for continuous structural metrics
  - Chi-square or Fisher’s exact tests for categorical sparsity indicators
  - Cliff’s delta for continuous effect sizes
  - Risk difference for categorical metrics
  - Bootstrap 95% confidence intervals for median and risk differences

- Applied Benjamini–Hochberg FDR correction across all structural tests

- Defined a structural result as “supported” only if:
  - qval_fdr < FDR_ALPHA
  - AND effect size >= predefined threshold (continuous or categorical)

- Produced structural test artifacts:
  - phase8_structural_tests.csv (full statistical table with q-values and support flags)

- Generated a consolidated structural summary artifact:
  - phase8_summary.json containing:
    - Query group sizes
    - Persistent proportions
    - Mean score gap (persistent)
    - Persistent sparsity percentage
    - Hardness comparison
    - Number of structural tests
    - Number of supported findings
    - List of supported structural metrics
    - Warning logs

- Identified supported structural drivers of persistent failures:
  - Extremely low num_relevant_1
  - High probability of exactly one relevant document
  - Strong negative score_gap (poor separability near rank-5 boundary)

- Confirmed that the following were NOT supported as consistent structural drivers:
  - num_docs (query length)
  - score_std_top10
  - Composite hardness (as an independent separator)


NOTE: Phase 8 does not introduce new models or alter evaluation criteria. Its purpose is to move beyond "which model performs better" and instead diagnose *why* certain queries fail persistently, using evidence-driven structural testing with multiple-comparison control and effect-size-aware interpretation.



***************************************************************************

Phase 9: Robustness & Generalization Validation (Completed)


The following steps have been completed:

- Validated whether key findings from Phases 6-8 remain stable under multiple robustness lenses, without retraining or altering any prior outputs

- Enforced strict Phase 9 constraints:
  - Used ONLY Phase 6 artifacts (query_metrics + predictions)
  - No retraining, no new feature engineering, no post-hoc score changes
  - No hidden changes to K values or relevance thresholds
  - Deterministic outputs and stable file naming
  - Association language only (no causal claims)

- Performed Cross-Dataset Persistent Comparison (MQ2007 vs MQ2008):
  - Recomputed persistent failures per dataset as:
    - Persistent = intersection of failures across all 9 model x pipeline configs
  - Preserved Phase 8 evaluability rule:
    - evaluable = num_relevant_1 > 0
  - Computed persistent rate summaries:
    - pct_persistent_of_failing
    - pct_persistent_of_evaluable
  - Applied statistical test for rate difference:
    - Chi-square if counts sufficient, otherwise Fisher exact
  - Emitted small-sample stability warnings when persistent group sizes were < MIN_SAMPLE_WARNING
  - Saved artifact:
    - phase9_persistent_cross_dataset.csv

- Conducted Threshold & K Sensitivity Analysis (Baseline-only):
  - Tested whether failure behavior changes when evaluation conditions change, without changing model training
  - Used baseline predictions only (pointwise_raw) per dataset
  - Recomputed Failure@K using prediction scores under:
    - K = {1, 3, 5, 10}
    - relevance_threshold = {label >= 1, label == 2}
  - Ensured robust evaluability handling:
    - Queries with zero relevant docs at threshold are marked non-evaluable
    - k_actual = min(k, n_docs) with safe guards for k <= 0
  - Produced tabular outputs and sensitivity plots per dataset
  - Saved artifacts:
    - phase9_threshold_sensitivity.csv
    - phase9_threshold_sensitivity_2007.png
    - phase9_threshold_sensitivity_2008.png

- Implemented Structural Replication Check (Phase 8 -> MQ2008):
  - Purpose: test whether Phase 8’s supported structural signals from MQ2007 persist in MQ2008
  - Loaded Phase 8 structural test list (phase8_structural_tests.csv) for transparency
  - Defined MQ2008 query groups using the same Phase 8 logic:
    - persistent = intersection across 9 configs (MQ2008)
    - successful = evaluable - all_failing
  - Prioritized replication of Phase 8-supported metrics:
    - num_relevant_1
    - pct_num_rel_eq_1
  - Re-ran statistical comparisons in MQ2008:
    - Mann–Whitney U for num_relevant_1
    - Chi-square or Fisher exact for pct_num_rel_eq_1
  - Applied BH-FDR correction over replication tests
  - Saved artifact:
    - phase9_structural_replication.csv

- Performed Score Calibration Sanity Check (ranking scores, not probabilities):
  - Verified whether higher normalized ranking scores correspond to higher observed relevance frequency
  - Normalized scores per query using min-max scaling
  - Binned normalized scores and computed:
    - mean_predicted (average normalized score per bin)
    - observed_frequency (relevance rate per bin using label ≥ 1)
  - Computed ECE-style summary for interpretability (sanity indicator only)
  - Generated reliability-style plots for MQ2007:
    - Baseline model
    - Best model (lightgbm_per_query) when available
  - Saved artifacts:
    - phase9_calibration_summary.csv
    - phase9_calibration_baseline.png
    - phase9_calibration_best_model.png

- Tested Statistical Robustness Across K (Paired McNemar for binary Failure@K):
  - Verified whether changes in Failure@K vs baseline remain stable when K changes
  - Evaluated for K = {3, 10} under relevance_threshold = label >= 1
  - Ensured paired alignment:
    - Comparisons restricted to common evaluable qids between baseline and config
  - Applied BH-FDR correction per (dataset, K)
  - Corrected McNemar fallback logic:
    - Used exact two-sided binomtest when statsmodels not available
  - Added explicit McNemar direction label:
    - improves if n10 > n01
    - worsens if n01 > n10
    - tie otherwise
  - Saved artifact:
    - phase9_statistical_robustness.csv

- Produced consolidated Phase 9 artifacts (Phase 10-ready):
  - CSV outputs:
    - phase9_persistent_cross_dataset.csv
    - phase9_threshold_sensitivity.csv
    - phase9_structural_replication.csv
    - phase9_calibration_summary.csv
    - phase9_statistical_robustness.csv
  - PNG outputs:
    - phase9_threshold_sensitivity_2007.png
    - phase9_threshold_sensitivity_2008.png
    - phase9_calibration_baseline.png
    - phase9_calibration_best_model.png

NOTE: Phase 9 does not introduce new models or alter evaluation criteria. Its purpose is to verify whether earlier conclusions are robust to dataset shift (MQ2007 -> MQ2008), evaluation sensitivity (K and relevance thresholds), and paired binary stability across K, while explicitly handling small-sample limitations and enforcing transparent replication boundaries.


************************************************************

Phase 10: Fold Robustness Validation (Completed)

The following steps have been completed:

- Verified whether the main findings of earlier phases remain stable when using different LETOR folds instead of relying only on Fold1

- Created fold-aware Phase 6 artifacts without modifying earlier results:
  - Re-ran the Phase 6 pipeline for MQ2007 Fold1, Fold2, and Fold3
  - Saved artifacts in a new structure:
    - phase6_models_folds/Fold1
    - phase6_models_folds/Fold2
    - phase6_models_folds/Fold3
  - Preserved the original flat Phase 6 outputs so that Phases 7–9 remain unchanged

- Enforced strict Phase 10 constraints:
  - No retraining logic changes
  - Same models and pipelines as Phase 6
  - Same Failure@5 definition
  - Same relevance rule (num_relevant_1 > 0 for evaluable queries)
  - Same deterministic seed and preprocessing
  - No feature engineering or parameter tuning

- Implemented a fold-aware artifact loader:
  - Loaded query_metrics and prediction files for each fold
  - Required exactly 9 configs per fold (3 models × 3 pipelines)
  - Validated required columns:
    - qid
    - num_docs
    - num_relevant_1
    - Failure@5_primary
    - label
    - score
  - Added dtype coercion to avoid qid / score type mismatches
  - Logged warnings if configs were missing

- Computed baseline failure rates per fold using the baseline configuration (pointwise_raw):
  - evaluable queries defined as num_relevant_1 > 0
  - failure defined using Failure@5_primary
  - Calculated:
    - number of evaluable queries
    - number of failures
    - percentage failure rate
  - Saved artifact:
    - phase10_fold_failure_rates.csv

- Identified persistent failures within each fold:
  - persistent defined as intersection of failures across all 9 configs
  - computed additional sets:
    - all_failing = queries failing in at least one config
    - successful = evaluable queries that never fail
  - calculated fold summaries:
    - n_evaluable
    - n_failing
    - n_persistent
    - n_successful
    - pct_persistent_of_failing
    - pct_persistent_of_evaluable
  - emitted warnings when sample sizes were small
  - saved artifact:
    - phase10_fold_persistent_summary.csv

- Performed structural direction validation across folds:
  - tested whether the structural signals discovered in Phase 8 Fold1 still point in the same direction
  - compared persistent vs successful queries using baseline artifacts
  - evaluated three structural signals:
    - num_relevant_1
    - sparsity (pct_num_rel_eq_1)
    - score_gap (best relevant score − rank-5 score)
  - applied statistical tests:
    - Mann–Whitney U for numeric metrics
    - Chi-square or Fisher exact for sparsity
  - recorded whether the direction matched the expected structural pattern
  - saved artifact:
    - phase10_fold_structural_direction.csv

- Conducted model direction validation (LightGBM vs baseline):
  - compared failure rates of:
    - baseline: pointwise_raw
    - stronger model: lightgbm_per_query
  - restricted comparison to common evaluable qids to ensure fair alignment
  - computed failure percentages for both models on the same query set
  - recorded whether LightGBM reduced failures relative to baseline
  - saved artifact:
    - phase10_fold_model_direction.csv

- Generated a consolidated Phase 10 experiment summary:
  - aggregated fold-level findings including:
    - baseline failure rates
    - persistent failure rates
    - structural direction consistency
    - number of tests performed
    - warning logs
  - saved artifact:
    - phase10_summary.json

NOTE: Phase 10 does not introduce new models or modify evaluation criteria. Its purpose is to check whether the key patterns discovered earlier (failure rates, persistent queries, and structural signals) remain stable when the experiment is repeated across multiple folds. This helps confirm that the findings are not just an artifact of one particular data split.