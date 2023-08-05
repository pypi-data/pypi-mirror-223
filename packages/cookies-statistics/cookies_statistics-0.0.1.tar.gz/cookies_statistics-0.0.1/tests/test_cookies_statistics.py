import pytest
import numpy as np
import cookies_statistics as cs


class TestCookiesStatistics:

    def test_lsq_householder(self):
        Z = np.array([[3., -2.], [0., 3.], [4.,  4.]])
        y = np.array([3., 5., 4.])
        a, s2 = cs.lsq_householder(Z, y)
        assert a[0] == pytest.approx(0.76)
        assert a[1] == pytest.approx(0.6)
        assert s2 == pytest.approx(4.0)
