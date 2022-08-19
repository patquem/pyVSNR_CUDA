"""
Main VSNR functions
"""
import os
from ctypes import windll, POINTER, c_int, c_float
import numpy as np

PRECOMPILED_PATH = os.path.join(__file__, "..", "precompiled")
NBLOCKS = 1024


def get_vsnr2d():
    """ Load the 'cuda' function from the dedicated .dll library"""
    dll = windll.LoadLibrary(os.path.join(PRECOMPILED_PATH, "libvsnr2d.dll"))
    func = dll.VSNR_2D_FIJI_GPU
    func.argtypes = [POINTER(c_float), c_int, POINTER(c_float),
                     c_int, c_int, c_int,
                     c_float, POINTER(c_float), c_int, c_float]
    return func


def vsnr2d(img, filters, nite=100, beta=1, nblocks=NBLOCKS):
    """
    Calculate the corrected image using the 2D-VSNR algorithm in libvsnr2d.dll

    .. note:
    To ease code comparison with original coding, most of the variable names
    have been kept as nearly as possible during the code transcription.
    Accordingly, PEP8 formatting compatibility is not always respected.

    Parameters
    ----------
    img: numpy.ndarray((n0, n1))
        The image to process
    filters: list of dicts
        Dictionaries that contains filters definition.
        Example For a 'Dirac' filter:
        - filter={'name':'dirac', 'noise_level':10}
        Example For a 'Gabor' filter:
        - filter={'name':'gabor', 'noise_level':5, 'sigma':(3, 40), 'theta':45}
    nite: int, optional
        Number of iterations in the denoising processing
    beta: float, optional
        Undefined parameters in the original code (no effect on the results ?)
    nblocks: int, optional
        Maximum number of threads per block to work with

    Returns
    -------
    img_corr: numpy.ndarray((n0, n1))
        The corrected image
    """
    length = len(filters)
    n0, n1 = img.shape

    # psis definition from filters
    psis = []
    for filt in filters:
        name = filt['name']
        noise_level = filt['noise_level']
        if name == 'dirac':
            psis += [0, noise_level]
        elif name == 'gabor':
            sigma = filt['sigma']
            theta = filt['theta']
            psis += [1, noise_level, sigma[0], sigma[1], theta]
        else:
            raise IOError(f"filter name '{name}' should be 'dirac' or 'gabor'")

    # flattened arrays and corresponding pointers definition
    psis = np.asarray(psis).flatten()
    u0 = img.flatten()
    u = np.zeros_like(u0)

    psis_p = (c_float * len(psis))(*psis)
    u0_p = (c_float * len(u0))(*u0)
    u_p = (c_float * len(u))(*u)

    # calculation
    vmax = u0.max()
    get_vsnr2d()(psis_p, length, u0_p, n0, n1, nite, beta, u_p, nblocks, vmax)

    # reshaping
    img_corr = np.array(u_p).reshape(n0, n1).astype(float)

    return img_corr
