import cv2
import numpy as np
import os
import codecs
import time
import math
from LocateKeyPoints.CalcMinInclusiveCir import *


def draw_random_sketch(zi, nlines, imgsize, start_p_cir, end_p_cir, start_p_radius, end_p_radius, minth, maxth , npics, strictness=1.0):
    # np.random.seed(int(time.time()))  # Fully random
    np.random.seed(1)  # For test only
    for idx in range(npics):
        outimg = np.zeros(shape=imgsize, dtype='uint8')
        for i in range(nlines):
            start_cir_c = start_p_cir[i]
            start_cir_r = start_p_radius[i]

            start_r = np.random.uniform(0, start_cir_r*strictness)
            start_arg = np.random.uniform(0, math.pi*2)

            start_vec = (math.sin(start_arg)*start_r, math.cos(start_arg)*start_r)
            start_p = (int(start_cir_c[0] + start_vec[0]), int(start_cir_c[1] + start_vec[1]))

            end_cir_c = end_p_cir[i]
            end_cir_r = end_p_radius[i]

            end_r = np.random.uniform(0, end_cir_r*strictness)
            end_arg = np.random.uniform(0, math.pi * 2)

            end_vec = (math.sin(end_arg) * end_r, math.cos(end_arg) * end_r)
            end_p = (int(end_cir_c[0] + end_vec[0]), int(end_cir_c[1] + end_vec[1]))

            cv2.line(outimg, start_p, end_p, 255, 3)

        outimg = cv2.bitwise_not(outimg)
        cv2.imwrite("./zi/%s/genSketch/%s.png" % (zi, idx), outimg)


if __name__ == "__main__":
    nlines, imgsize, start_p_cir, end_p_cir, start_p_radius, end_p_radius, minth, maxth = calc_min_inc_cir("tian")
    npics = 100
    draw_random_sketch("tian", nlines, (512, 512), start_p_cir, end_p_cir, start_p_radius, end_p_radius, minth, maxth, npics, 0.5)
