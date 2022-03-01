import cv2
import numpy as np
import os
import codecs


def bw_reserve(img):
    x = img.shape[0]
    y = img.shape[1]
    out = np.zeros(shape=img.shape, dtype='uint8')
    for i in range(x):
        for j in range(y):
            out[i][j] = 255 - img[i][j]

    return out


def draw_source_img_sketch(zi):
    # zi = "bu"  # あとで、MAINファンクションのパラメータの形式に変えて
    imgsize = (512, 512)
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
    fs = 1

    for f in logfiles:
        outimg = np.zeros(shape=imgsize, dtype='uint8')
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


            cv2.line(outimg, (sx1, sy1), (ex1, ey1), 255, 3)

            idx = idx + 1
        outimg = cv2.bitwise_not(outimg)
        cv2.imwrite("./zi/%s/sourceSketch/%s.png" % (zi, f.replace(".txt", "S")), outimg)
        fs = fs + 1


if __name__ == "__main__":
    draw_source_img_sketch("tian")
