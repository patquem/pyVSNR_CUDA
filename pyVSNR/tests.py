"""
unittest
"""
import unittest
import numpy as np

from pyVSNR.examples import ex_camera_stripes, ex_camera_curtains


class TestVSNR(unittest.TestCase):
    """
    Test VSNR algorithm
    """

    def test_ex_camera_stripes(self):
        """ Test VSNR algorithm on stripes removal """

        img_corr = ex_camera_stripes()

        self.assertAlmostEqual(np.sum(img_corr), 132656.64509357885)

    def test_ex_camera_curtains(self):
        """ Test VSNR algorithm on curtains removal """

        img_corr = ex_camera_curtains()

        self.assertAlmostEqual(np.sum(img_corr), 121879.02824494091)
