Documentation
=============

Functions
*********

cookies_statistics.backsub
--------------------------

.. autofunction:: cookies_statistics.backsub

cookies_statistics.upper_triangularize
--------------------------------------

.. autofunction:: cookies_statistics.upper_triangularize

cookies_statistics.lsq_householder
----------------------------------

.. autofunction:: cookies_statistics.lsq_householder

**Example**

.. code-block:: python

   import numpy as np
   import cookies_statistics as cs

   Z = np.array([[3., -2.], [0., 3.], [4.,  4.]])
   y = np.array([3., 5., 4.])
   print(cs.lsq_householder(Z, y))
   #  --> (array([0.76, 0.6 ]), 4.0)

Classes
*******

