Compiler IR
===========

IRNode
------

opcode

inputs

outputs

attributes


IR operations
=============

1. ExtractFeatureColumn
-----------------------

Input

    X
    samples[]
    feature_index

Output

    feature_values[]

Equivalent implementation

    sort_samples_and_feature_values()


2. SortSamples
--------------

Input

    feature_values[]
    samples[]

Output

    sorted feature_values[]
    reordered samples[]

Equivalent implementation

    simultaneous_sort()


3. EvaluateSplit
----------------

Input

    feature_values[]
    samples[]
    criterion

Process

    enumerate thresholds

    move samples from right → left

    update criterion statistics

    compute impurity improvement

Output

    SplitRecord

Equivalent implementation

    next_p()

    criterion.update()

    proxy_impurity_improvement()

    children_impurity()

    impurity_improvement()


4. PartitionSamples
-------------------

Input

    samples[]
    SplitRecord

Output

    reordered samples[]

Equivalent implementation

    partition_samples_final()


5. CreateNode
-------------

Input

    ParentInfo
    SplitRecord

Output

    Tree node

Equivalent implementation

    _add_node()


Data structures
===============

samples[]

    reordered row indices

feature_values[]

    temporary feature buffer

ParentInfo

    node metadata inherited during traversal

SplitRecord

    selected split metadata

Tree

    output model representation