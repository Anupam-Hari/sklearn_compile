RandomForestClassifier.fit()

Estimator layer
---------------

sklearn/ensemble/_forest.py

    fit() -> line 303

Algorithm layer
---------------

sklearn/tree/_classes.py

    _fit() -> line 238

Primitive layer
---------------

sklearn/tree/_tree.pyx

    DepthFirstTreeBuilder -> line 146

    BestFirstTreeBuilder -> line 399

sklearn/tree/_splitter.pyx

    node_split_best() -> line 266

    BestSplitter -> line 738

sklearn/tree/_criterion.pyx

    Gini -> line 605

sklearn/tree/_partitioner.pyx

    sort_samples_and_feature_values() -> line 75

    next_p() -> line 300

    partition_samples_final() -> line 390

Builder instantiation

_classes.py

    DepthFirstTreeBuilder -> line 547

    BestFirstTreeBuilder -> line 556

Execution path

RandomForestClassifier.fit()
    _forest.py:303

        ↓

DecisionTreeClassifier._fit()
    _classes.py:238

        ↓

builder = DepthFirstTreeBuilder()
    _classes.py:547

or

builder = BestFirstTreeBuilder()
    _classes.py:556

        ↓

builder.build()
    _classes.py:566

Files involved
--------------

Estimator

    sklearn/ensemble/_forest.py

Algorithm

    sklearn/tree/_classes.py

Primitives

    sklearn/tree/_tree.pyx

    sklearn/tree/_splitter.pyx

    sklearn/tree/_criterion.pyx

    sklearn/tree/_partitioner.pyx

Generated C++ kernels (future)

------------------------------

Tree

    Node representation

    Tree storage

    Tree traversal

Splitter

    Best split search

    Feature selection

    Threshold enumeration

Criterion

    Gini impurity

Partitioner

    Sample sorting

    Sample partitioning

Compiler dependency order

-------------------------

_tree.pyx

    depends on:

        _splitter.pyx

_splitter.pyx

    depends on:

        _criterion.pyx

        _partitioner.pyx

_criterion.pyx

    independent

_partitioner.pyx

    independent

_classes.py

    depends on:

        _tree.pyx

_forest.py

    depends on:

        _classes.py
