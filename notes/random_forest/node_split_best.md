node_split_best()

    initialize split search

    initialize best_split

    initialize current_split

    select candidate features

    while candidate features remain:

        select next feature

        sort samples by feature value

        initialize criterion

        while candidate thresholds remain:

            move samples from right partition to left partition

            update criterion statistics

            compute impurity improvement

            if improvement > current best:

                store split

        evaluate missing values

        finalize best threshold for this feature

    reorder samples according to the best split

    return best_split

| Function | File | Responsibility |
| -------- | ---- | -------------- |
| sort_samples_and_feature_values() | _partitioner.pyx | feature sorting |
| next_p() | _partitioner.pyx | threshold enumeration |
| partition_samples_final() | _partitioner.pyx | sample partitioning |
| reset() | _criterion.pyx | criterion initialization |
| update() | _criterion.pyx | incremental statistics |
| proxy_impurity_improvement() | _criterion.pyx | candidate split scoring |
| children_impurity() | _criterion.pyx | child impurity calculation |
| impurity_improvement() | _criterion.pyx | final split evaluation |

Data model

X               -> original feature matrix (never reordered)

samples[]        -> row indices

feature_values[] -> temporary buffer containing one feature column

----------------------------------------------------------

Example

X:

row 0 -> [5.1]
row 1 -> [1.3]
row 2 -> [3.7]
row 3 -> [2.4]

samples:

[0, 1, 2, 3]

feature_values after extraction:

[5.1, 1.3, 3.7, 2.4]

feature_values after sorting:

[1.3, 2.4, 3.7, 5.1]

samples after simultaneous sorting:

[1, 3, 2, 0]