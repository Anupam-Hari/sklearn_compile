RandomForestClassifier.fit()

sklearn/ensemble/_forest.py
--------------------------------------------------

RandomForestClassifier
    ↓
ForestClassifier
    ↓
BaseForest.fit()
    ↓
_parallel_build_trees()
    ↓
DecisionTreeClassifier._fit()

--------------------------------------------------

Decision tree subsystem

sklearn/tree/_classes.py
--------------------------------------------------

BaseDecisionTree._fit()
    ↓
DepthFirstTreeBuilder.build()

--------------------------------------------------

Tree builder subsystem

sklearn/tree/_tree.pyx
--------------------------------------------------

DepthFirstTreeBuilder.build()
    ↓
splitter.node_split()

--------------------------------------------------

Splitter subsystem

sklearn/tree/_splitter.pyx
--------------------------------------------------

BestSplitter.node_split()
    ↓
node_split_best()

--------------------------------------------------

Partitioning subsystem

sklearn/tree/_partitioner.pyx
--------------------------------------------------

sort_samples_and_feature_values()

next_p()

partition_samples_final()

--------------------------------------------------

Criterion subsystem

sklearn/tree/_criterion.pyx
--------------------------------------------------

Gini

reset()

update()

proxy_impurity_improvement()

children_impurity()

impurity_improvement()

Files required for RandomForestClassifier.fit()

Tier 1: Forest layer (entry point)

sklearn/ensemble/_forest.py

Responsibilities:

- RandomForestClassifier
- ForestClassifier
- BaseForest.fit()
- _parallel_build_trees()

--------------------------------------------------

Tier 2: Tree API layer

sklearn/tree/_classes.py

Responsibilities:

- DecisionTreeClassifier
- BaseDecisionTree._fit()

--------------------------------------------------

Tier 3: Tree construction layer

sklearn/tree/_tree.pyx
sklearn/tree/_tree.pxd

Responsibilities:

- Tree
- TreeBuilder
- DepthFirstTreeBuilder
- BestFirstTreeBuilder

--------------------------------------------------

Tier 4: Split selection layer

sklearn/tree/_splitter.pyx
sklearn/tree/_splitter.pxd

Responsibilities:

- Splitter
- BestSplitter
- RandomSplitter
- node_split_best()

--------------------------------------------------

Tier 5: Sample partitioning layer

sklearn/tree/_partitioner.pyx
sklearn/tree/_partitioner.pxd

Responsibilities:

- DensePartitioner
- SparsePartitioner

--------------------------------------------------

Tier 6: Impurity layer

sklearn/tree/_criterion.pyx
sklearn/tree/_criterion.pxd

Responsibilities:

- Criterion
- Gini
- Entropy
- LogLoss

--------------------------------------------------

Tier 7: Utilities

sklearn/tree/_utils.pyx
sklearn/tree/_utils.pxd

Responsibilities:

- Low-level helper functions