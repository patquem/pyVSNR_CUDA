"""
Examples of VSNR algorithm applications
"""
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread, imsave

from pyVSNR import vsnr2d

DATA_PATH = os.path.join(__file__, "..", "data")
SAVE_IMG = False


def camera_process(img_label, filters, show_plot=False):
    img = imread(os.path.join(DATA_PATH, f"{img_label}.tif"))
    img_ref = imread(os.path.join(DATA_PATH, "camera.tif"))

    return img_process(img_label, filters, img, img_ref, show_plot=show_plot)


def ex_camera_gaussian_noise(noise_level=0.32,
                             show_plot=False):
    """
    Example of gaussian noise removal from 'camera' image
    """
    filters = [{'name': 'Dirac', 'noise_level': noise_level}]

    return camera_process('camera_gaussian_noise', filters, show_plot=show_plot)


def ex_camera_stripes(noise_level=100, sigma=(1000, 0.1), theta=0,
                      show_plot=False):
    """
    Example of stripes removal from 'camera' image
    """
    filters = [{'name': 'Gabor',
                'noise_level': noise_level, 'sigma': sigma, 'theta': theta}]

    return camera_process('camera_stripes', filters, show_plot=show_plot)


def ex_camera_curtains(noise_level=20, sigma=(3, 40), theta=0,
                       show_plot=False):
    """
    Example of curtains removal from 'camera' image
    """
    filters = [{'name': 'Gabor',
                'noise_level': noise_level, 'sigma': sigma, 'theta': theta}]

    return camera_process('camera_curtains', filters, show_plot=show_plot)


def ex_fib_sem(noise_level=30, sigma=(1, 30), theta=358,
               show_plot=False):
    """
    Example of curtains removal from a real FIB-SEM image
    """
    img_label = "fib_sem"
    img = imread(os.path.join(DATA_PATH, "fib_sem.tif"))

    filters = [{'name': 'Gabor',
                'noise_level': noise_level, 'sigma': sigma, 'theta': theta}]

    return img_process(img_label, filters, img, None, show_plot=show_plot)


def img_process(img_label, psis, img, img_ref, show_plot=False):
    """ Image processing"""
    print(f"{img_label}...", end=" ")

    # vsnr processing
    t0 = time.process_time()
    img_corr = vsnr2d(img, psis, nite=20)
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
        imsave(os.path.join(DATA_PATH, f"{img_label}_corr.tif"), img_corr)
        fig.savefig(os.path.join(DATA_PATH, f"{img_label}_comp.png"))

    if show_plot:
        plt.show()

    return img_corr


if __name__ == '__main__':
    ex_camera_gaussian_noise()
    ex_camera_stripes()
    ex_camera_curtains()
    ex_fib_sem()
    plt.show()
