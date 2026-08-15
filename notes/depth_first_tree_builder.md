DepthFirstTreeBuilder.build()

    validate input

    allocate tree storage

    initialize splitter

    initialize root node

    push root node onto stack

    while stack is not empty:

        pop node from stack

        reset splitter for current node

        determine stopping conditions

        compute node impurity

        if node is not a leaf:

            find the best split

        create a new tree node

        store node prediction values

        if node is not a leaf:

            compute child constraints

            push right child onto stack

            push left child onto stack

    resize tree to final size

    store maximum depth

    return

Important data structures

Tree

    stores all nodes

Splitter

    owns the current sample partition

StackRecord

    start

    end

    depth

    parent

    is_left

    impurity

    n_constant_features

    lower_bound

    upper_bound

ParentInfo

    impurity

    n_constant_features

    lower_bound

    upper_bound

SplitRecord

    feature

    threshold

    pos

    improvement

    impurity_left

    impurity_right

    missing_go_to_left

build() dependencies

node_reset()

    initialize the current node inside the splitter

node_impurity()

    compute the impurity of the current node

node_split()

    find the best split for the current node

_add_node()

    append a node to the tree structure

SplitRecord

    stores the selected split

ParentInfo

    stores information propagated from the parent node

ParentInfo

    impurity

    n_constant_features

    lower_bound

    upper_bound

SplitRecord

    feature

        feature chosen for the split

    pos

        split position inside samples[]

    threshold

        numerical split threshold

    left_cat_bitset

        categories assigned to the left child

    improvement

        impurity improvement

    impurity_left

        left child impurity

    impurity_right

        right child impurity

    lower_bound

        monotonic lower bound

    upper_bound

        monotonic upper bound

    missing_go_to_left

        missing-value routing flag

node_reset()

    receives:

        start

        end

    updates:

        splitter.start

        splitter.end

    initializes:

        criterion.init()

    computes:

        weighted_n_node_samples

_add_node()

    receives:

        parent

        is_left

        is_leaf

        feature

        threshold

        impurity

        n_node_samples

        weighted_n_node_samples

        missing_go_to_left

    allocates:

        Node

    appends:

        node -> tree.nodes[]