import cv2
import numpy as np
import os
import codecs
import math


'''
    二点でベクトルの角度を計算して (0~2pi)
'''
def calc_arg_by_2points(p1, p2):
    vec = (p2[0]-p1[0], p2[1]-p1[1])
    r = math.hypot(vec[0], vec[1])
    if r == 0:
        r = 1
    x = vec[0]
    y = vec[1]
    costh = x/r
    sinth = y/r
    if costh>=0 and sinth>=0:
        arg = math.acos(costh)
    if costh<0 and sinth>=0:
        arg = math.acos(costh)
    if costh<0 and sinth<0:
        arg = math.pi*2 - math.acos(costh)
    if costh>=0 and sinth<0:
        arg = math.pi*2 - math.acos(costh)

    return arg


def calc_min_inc_cir(zi):
    # zi = "bu"  # あとで、MAINファンクションのパラメータの形式に変えて
    imgsize = (512, 512, 3)
    log_path_prefix = "./zi/%s/logs/" % zi
    logfiles = os.listdir(log_path_prefix)
    '''
        いくつのキーポイントがあるを調べる
    '''
    res = []
    nlines = len(codecs.open(log_path_prefix + logfiles[0], "r", "utf-8").readlines())
    print(nlines)
    for i in range(nlines):
        temp = [[], []]
        res.append(temp)

    '''
        一応、中間点を置きっぱなし
    '''
    minth = [math.inf] * nlines  # 筆画の最小輻射角度
    maxth = [-math.inf] * nlines
    for f in logfiles:
        print(f)
        fin = codecs.open(log_path_prefix + f, "r", "utf-8")
        '''
            LINEを一つずつ読み込む
        '''
        lines = fin.readlines()
        idx = 0
        for line in lines:
            line = line.strip()
            startp = line.split(";")[0]  # 初めの点
            endp = line.split(";")[-1]  # 最後の点
            '''
                STR TO INT-DATA 
            '''
            sx1 = int(startp.split(",")[0])
            sy1 = int(startp.split(",")[-1])
            ex1 = int(endp.split(",")[0])
            ey1 = int(endp.split(",")[-1])
            if max(sx1, sy1, ex1, ey1) > 512:
                print("OUT OF RANGE ||%s" % f)
            res[idx][0].append([sx1, sy1])
            res[idx][1].append([ex1, ey1])

            current_arg = calc_arg_by_2points([sx1, sy1], [ex1, ey1])  # このペアの点に作るベクトルの輻射角度
            minth[idx] = min(minth[idx], current_arg)
            maxth[idx] = max(maxth[idx], current_arg)

            idx = idx + 1

    '''
        最小包囲圓を計算して
    '''
    start_p_cir = []  # 筆画の起点の圓の円心
    end_p_cir = []
    start_p_radius = []  # 筆画の起点の圓の半径
    end_p_radius = []


    for i in range(nlines):
        scc, sr = cv2.minEnclosingCircle(np.array(res[i][0]))
        ecc, er = cv2.minEnclosingCircle(np.array(res[i][1]))
        start_p_cir.append(scc)
        start_p_radius.append(sr)
        end_p_cir.append(ecc)
        end_p_radius.append(er)

    return nlines, imgsize, start_p_cir, end_p_cir, start_p_radius, end_p_radius, minth, maxth


'''
    それら圓をえがく
'''
def show_sample(nlines, imgsize, start_p_cir, end_p_cir, start_p_radius, end_p_radius):

    outimg = np.zeros(shape=imgsize, dtype='uint8')
    for i in range(nlines):
        cv2.circle(outimg, (int(start_p_cir[i][0]), int(start_p_cir[i][1])), int(start_p_radius[i]), (255, 0, 0), 2)
        cv2.circle(outimg, (int(end_p_cir[i][0]), int(end_p_cir[i][1])), int(end_p_radius[i]), (0, 0, 255), 2)
        cv2.line(outimg, (int(start_p_cir[i][0]), int(start_p_cir[i][1])), (int(end_p_cir[i][0]), int(end_p_cir[i][1])), (0, 255, 0), 2)

    cv2.namedWindow("imshow")
    cv2.imshow("imshow", outimg)
    cv2.waitKey(0)
    pass


def main():
    nlines, imgsize, start_p_cir, end_p_cir, start_p_radius, end_p_radius, minth, maxth = calc_min_inc_cir("tian")
    print(minth)
    print(maxth)
    show_sample(nlines, imgsize, start_p_cir, end_p_cir, start_p_radius, end_p_radius)


if __name__ == "__main__":
    main()


