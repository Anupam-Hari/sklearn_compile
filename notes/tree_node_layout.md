Tree node layout
================

Node creation
-------------

_add_node()

    allocate Node

    initialize impurity

    initialize sample counts

    connect to parent

    if leaf:

        left_child  = LEAF

        right_child = LEAF

        feature     = UNDEFINED

        threshold   = UNDEFINED

    else:

        feature = selected feature

        threshold = selected threshold

        missing_go_to_left = selected missing-value policy

    append node to tree.nodes[]

Tree storage model
==================

tree.nodes[]

    contiguous array

        node[0] = root

        node[1] = child

        node[2] = child

        ...

Each node stores

    left_child

    right_child

    feature

    threshold

    impurity

    n_node_samples

    weighted_n_node_samples

    missing_go_to_left

Prediction algorithm
====================

apply()

    for each sample:

        node = root

        while node is not a leaf:

            read feature value

            evaluate split condition

            if condition is true:

                node = left child

            else:

                node = right child

        return leaf node

Tree object
===========

Tree metadata
-------------

n_features

n_classes

n_outputs

max_n_classes

n_categories

max_depth

node_count

capacity

Tree storage
------------

nodes

    Node*

value

    float64_t*

value_stride


Node creation
-------------

_add_node()

    inputs:

        parent

        is_left

        is_leaf

        feature

        threshold

        left_cat_bitset

        impurity

        n_node_samples

        weighted_n_node_samples

        missing_go_to_left

    operations:

        allocate node

        connect node to parent

        initialize node fields

        append node to tree.nodes[]

Prediction
----------

predict()

    apply()

        _apply_dense()

            start at root node

            while current node is not a leaf:

                read feature value

                evaluate split condition

                move to left or right child

            return leaf node

        use leaf node to retrieve prediction from tree.value[]

Memory layout
=============

Node metadata is stored in:

    nodes[]

Predicted values are stored separately in:

    value[]

Tree structure and prediction values are intentionally decoupled.

Node
====

struct Node
-----------

left_child

    index of the left child inside tree.nodes[]

right_child

    index of the right child inside tree.nodes[]

feature

    feature used for the split

threshold

    numerical split threshold

left_cat_bitset

    bitset representing categories assigned to the left child

impurity

    node impurity

n_node_samples

    number of samples reaching this node

weighted_n_node_samples

    weighted sample count

missing_go_to_left

    missing-value routing policy

Memory representation
=====================

tree.nodes[]

    node 0

        left_child = 1

        right_child = 2

        feature = 3

        threshold = 5.4

    node 1

        ...

    node 2

        ...

tree.value[]

    node 0 prediction

    node 1 prediction

    node 2 prediction

Training pipeline
=================

X

    ↓

RandomForest.fit()

    ↓

DecisionTree._fit()

    ↓

TreeBuilder.build()

    ↓

Splitter

    ↓

Criterion

    ↓

Partitioner

    ↓

SplitRecord

    ↓

Tree._add_node()

    ↓

tree.nodes[]

    +

tree.value[]