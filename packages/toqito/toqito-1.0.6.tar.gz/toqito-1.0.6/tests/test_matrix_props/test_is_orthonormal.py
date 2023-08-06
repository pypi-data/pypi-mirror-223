"""Test is_orthonormal."""
import numpy as np

from toqito.matrix_props import is_orthonormal


def test_is_not_orthonormal():
    """This set of vectors are mutually orthogonal, but not orthonormal."""
    vec_1 = np.array([1, 0, -1])
    vec_2 = np.array([1, np.sqrt(2), 1])
    vec_3 = np.array([1, -np.sqrt(2), 1])

    vectors = np.array([vec_1, vec_2, vec_3])

    assert not is_orthonormal(vectors)


def test_is_orthonormal():
    """This set of vectors are orthonormal."""
    vec_1 = np.array([1 / np.sqrt(2), 1 / np.sqrt(2), 0])
    vec_2 = np.array([1 / np.sqrt(2), -1 / np.sqrt(2), 0])
    vec_3 = np.array([0, 0, 1])

    vectors = np.array([vec_1, vec_2, vec_3])

    assert is_orthonormal(vectors)


if __name__ == "__main__":
    np.testing.run_module_suite()
