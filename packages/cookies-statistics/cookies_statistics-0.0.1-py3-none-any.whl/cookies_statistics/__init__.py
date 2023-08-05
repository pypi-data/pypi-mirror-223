import numpy as np


def backsub(A, b):
    """ Solves Ax=b using back substitution.

        :param np.array A: A nxn upper triangular matrix.
        :param np.array b: A vector of length n.
        :rtype: np.array
    """
    m = A.shape[0]
    x = np.zeros(m)
    for i in reversed(range(m)):
        x_ = b[i]
        for j in range(i + 1, m):
            x_ -= A[i, j] * x[j]
        x[i] = x_ / A[i, i]
    return x


def upper_triangularize(X):
    """ This function repeatedly applies Householder transformations
        to A nxm matrix X (n >= m) until it becomes
        an upper triangular matrix, and then returns it.

        :param np.array X: A nxm matrix (n >= m).
        :rtype: np.array
    """
    n, m = X.shape
    for j in range(m):
        x = X[j:,j]
        target = np.zeros(n - j)
        target[0] = np.linalg.norm(x)
        u = x - target
        u = u / np.linalg.norm(u)
        if j > 0:
            u = np.concatenate((np.zeros(j), u))
        H = np.identity(n) - 2.0 * np.outer(u, u)
        X = H @ X
    return X


def lsq_householder(Z, y):
    """ Solve the least squares problem using Householder transformations.
        This function returns a tuple of the coefficient vector
        and the sum of squared errors.

        :param np.array Z: A Nxm data matrix (N >= m).
        :param np.array y: A vector of length N.
        :rtype: np.array, float
    """
    N, m = Z.shape
    X = np.hstack((Z, y.reshape([-1, 1])))
    X = upper_triangularize(X)
    return backsub(X[:m, :m], X[:m, m]), X[m, m]
