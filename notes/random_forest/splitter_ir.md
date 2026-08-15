SplitSearchIR

Inputs:

- X
- samples[]
- criterion
- min_samples_leaf
- min_weight_leaf
- max_features

--------------------------------------------------

FeatureSelectionIR

Inputs:

- samples[]
- feature_index

Outputs:

- feature_values[]
- sorted_samples[]

--------------------------------------------------

ThresholdEnumerationIR

Inputs:

- feature_values[]

Outputs:

- threshold_positions[]

--------------------------------------------------

CriterionUpdateIR

Inputs:

- threshold_position

Outputs:

- left_statistics
- right_statistics
- impurity

--------------------------------------------------

BestSplitIR

Inputs:

- impurity
- threshold
- feature

Outputs:

- best_feature
- best_threshold
- best_improvement

--------------------------------------------------

PartitionIR

Inputs:

- samples[]
- best_split

Outputs:

- reordered_samples[]

CriterionState

sum_total[]

sum_left[]

sum_right[]

weighted_n_node_samples

weighted_n_left

weighted_n_right

n_classes[]

--------------------------------------------------

Gini impurity

gini = 1 - Σ(p²)

where:

p = class_count / node_sample_count

--------------------------------------------------

NodeImpurityIR

Inputs:

- sum_total[]
- weighted_n_node_samples

Output:

- node_impurity

--------------------------------------------------

ChildrenImpurityIR

Inputs:

- sum_left[]
- sum_right[]
- weighted_n_left
- weighted_n_right

Outputs:

- impurity_left
- impurity_right