import numpy as np
import math
import random
import sys
from PIL import Image
from kd_tree import KDTree

sys.setrecursionlimit(9000)

def get_neighbors(pix, pixels, h):
    """Get neignbors of a particular point.
    Args:
        pos (int): the pixel position
        h (int): window size
        pixels (list): pixels
        num_cols (int): the number of columns in the image 
        num_rows (int): the number of rows in the image 
    Returns:
        list : a list of points
    """
    return pixels.get_neighbors(pix, h ** 2)

def manhattan(p1, p2):
    dist = 0
    dim = len(p1)
    for d in range(dim):
        dist += (p1[d] - p2[d]) ** 2
    return dist 

def get_mean_shift(pix, points, d):
    """Compute mean shift of a pixel.
    Args:
        pix (int): a pixel value
        points (list): neighbors of the pix
        d (int): distance
    Returns:
        float : a mean shift value
    """
    if len(points) == 0:
        raise ValueError("the neighbors is empty!")

    denom = 0
    num = [0, 0, 0]
    h2 = d ** 2 
    for p in points:
        dist = manhattan(pix, p)
        n = math.exp(-1 * dist / h2)
        num[0] += p[0] * n
        num[1] += p[1] * n
        num[2] += p[2] * n
        denom += math.exp(-1 * dist / h2)
    return (round(num[0] / denom), round(num[1] / denom), round(num[2] / denom))

def set_label(pixels):
    clust = set()
    for pix in pixels:
        clust.add(pix)

    colors = {}
    for i, v in enumerate(clust):
        colors[key] = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)) 
    for i, pix in enumerate(pixels):
        pixels[i] = colors[pix]
    return pixels

def unflatten(pixels, num_cols):
    length = len(pixels)
    arr = []
    for i in range(0, length, num_cols):
        arr.append(pixels[i: i+num_cols])
    return arr

def build_tree(pixels):
    kdt = KDTree(3)
    for pix in pixels:
        kdt.insert(pix)
    return kdt 

def get_delta(p1, p2):
    delta = 0
    dim = len(p1)
    for d in range(dim):
        delta += (p1[d] - p2[d]) ** 2
    return delta ** 0.5

def main():
    random.seed(1)
    h = 35
    stop_delta = 0.5
    im = Image.open('lenna_color.jpeg')
    num_cols, num_rows = im.size
    pix_arr = list(im.getdata())
    pixels = pix_arr
    kdt = build_tree(pixels)
    num_pixels = num_cols * num_rows 
    while (True):
        deltas = 0
        for i, pix in enumerate(pixels):
            neighbors = get_neighbors(pix, kdt, h)
            m = get_mean_shift(pix, neighbors, h)
            deltas += get_delta(pix, m) 
            pixels[i] = m
        print(deltas / num_pixels)
        if deltas / num_pixels < stop_delta:
            break
    pixels2d = unflatten(pixels, num_cols)
    result = Image.fromarray(np.array(pixels2d, dtype=np.uint8))
    result.save('result_color2.jpeg')

if __name__ == '__main__':
    main()

