"""
Examples of VSNR algorithm applications
"""
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread, imsave

from pyVSNR import vsnr2d

DATA_PATH = os.path.join(__file__, "data")
SAVE_IMG = False


def ex_camera_stripes(noise_level=0.5):
    """
    Example of stripes removal from 'camera' image
    """
    img_label = "camera_stripes"
    img = imread(os.path.join(DATA_PATH, "camera_stripes.tif"))
    img_ref = imread(os.path.join(DATA_PATH, "camera.tif"))

    # filter definition (1 dirac filter)
    filters = [{'name': 'dirac', 'noise_level': noise_level}]

    return img_process(img_label, filters, img, img_ref)


def ex_camera_curtains(noise_level=20, sigma=(3, 40), theta=0):
    """
    Example of curtains removal from 'camera' image
    """
    img_label = "camera_curtains"
    img = imread(os.path.join(DATA_PATH, "camera_curtains.tif"))
    img_ref = imread(os.path.join(DATA_PATH, "camera.tif"))

    # filter definition (1 gabor filter)
    filters = [{'name': 'gabor',
                'noise_level': noise_level, 'sigma': sigma, 'theta': theta}]

    return img_process(img_label, filters, img, img_ref)


def ex_fib_sem(noise_level=30, sigma=(1, 30), theta=358):
    """
    Example of curtains removal from a real FIB-SEM image
    """
    img_label = "fib_sem"
    img = imread(os.path.join(DATA_PATH, "fib_sem.tif"))
    img_ref = None

    # filter definition (1 gabor filter)
    filters = [{'name': 'gabor',
                'noise_level': noise_level, 'sigma': sigma, 'theta': theta}]

    return img_process(img_label, filters, img, img_ref)


def img_process(img_label, psis, img, img_ref):
    """ Image processing"""
    print(f"{img_label}...", end=" ")

    # vsnr processing
    t0 = time.process_time()
    img_corr = vsnr2d(img, psis, beta=1., nite=100)
    print("CGPU running time :", time.process_time() - t0)

    # image renormalization
    img_corr = np.clip(img_corr, img.min(), img.max())

    # plotting
    if img_ref is None:
        fig = plt.figure(figsize=(12, 6))
        plt.subplot(121)
        plt.title("Original")
        plt.imshow(img, cmap='gray')
        plt.subplot(122)
        plt.title("Corrected")
        plt.imshow(img_corr, cmap='gray')
        plt.tight_layout()
    else:
        fig = plt.figure(figsize=(14, 4))
        plt.subplot(131)
        plt.title("Reference")
        plt.imshow(img_ref)
        plt.subplot(132)
        plt.title("Reference + noise")
        plt.imshow(img)
        plt.subplot(133)
        plt.title("Corrected")
        plt.imshow(img_corr)
        plt.tight_layout()

    if SAVE_IMG:
        imsave(os.path.join(DATA_DIR, f"{img_label}_corr.tif"), img_corr)
        fig.savefig(os.path.join(DATA_DIR, f"{img_label}_comp.png"))

    return img_corr


if __name__ == '__main__':
    ex_camera_stripes()
    ex_camera_curtains()
    ex_fib_sem()
    plt.show()
