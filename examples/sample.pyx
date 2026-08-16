"""Example Cython code for testing the transpiler."""


cdef class TreeNode:
    """A simple tree node used in decision tree building."""
    
    cdef public int node_id
    cdef public double threshold
    cdef public int feature
    
    def __init__(self, int node_id, double threshold, int feature):
        self.node_id = node_id
        self.threshold = threshold
        self.feature = feature
    
    cpdef double evaluate_split(self, double[:] feature_values):
        """Evaluate a split on feature values."""
        cdef int n = feature_values.shape[0]
        cdef double total = 0.0
        cdef int i
        
        for i in range(n):
            if feature_values[i] < self.threshold:
                total += feature_values[i] * 0.5
            else:
                total += feature_values[i] * 2.0
        
        return total / n
    
    cdef void _reset(self):
        """Reset the node state."""
        self.node_id = -1
        self.threshold = 0.0
        self.feature = -1
