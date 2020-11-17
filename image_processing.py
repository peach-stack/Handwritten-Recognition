# 图像处理
import numpy as np
import queue
from tqdm import tqdm
import cv2
import os
from tqdm import tqdm
import pickle
#连通域算法进行图片切割
# 获取图片中各个小分割图像的坐标范围，data代表着待分割图像的灰度值矩阵，n_lines是表示分割图像中符号的行数
def get_x_y_cuts(data, n_lines=1):
    w, h = data.shape
    visited = set()
    q = queue.Queue()
    offset = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    cuts = []
    for y in range(h):
        for x in range(w):
            x_axis = []
            y_axis = []
            if data[x][y] < 200 and (x, y) not in visited:
                q.put((x, y))
                visited.add((x, y))
            while not q.empty():
                x_p, y_p = q.get()
                for x_offset, y_offset in offset:
                    x_c, y_c = x_p + x_offset, y_p + y_offset
                    if (x_c, y_c) in visited:
                        continue
                    visited.add((x_c, y_c))
                    try:
                        if data[x_c][y_c] < 200:
                            q.put((x_c, y_c))
                            x_axis.append(x_c)
                            y_axis.append(y_c)
                    except:
                        pass
            if x_axis:
                min_x, max_x = min(x_axis), max(x_axis)
                min_y, max_y = min(y_axis), max(y_axis)
                if max_x - min_x > 3 and max_y - min_y > 3:
                    cuts.append([min_x, max_x + 1, min_y, max_y + 1])
    if n_lines == 1:
        cuts = sorted(cuts, key=lambda x: x[2])
        pr_item = cuts[0]
        count = 1
        len_cuts = len(cuts)
        new_cuts = [cuts[0]]
        pr_k = 0
        for i in range(1, len_cuts):
            pr_item = new_cuts[pr_k]
            now_item = cuts[i]
            if not (now_item[2] > pr_item[3]):
                new_cuts[pr_k][0] = min(pr_item[0], now_item[0])
                new_cuts[pr_k][1] = max(pr_item[1], now_item[1])
                new_cuts[pr_k][2] = min(pr_item[2], now_item[2])
                new_cuts[pr_k][3] = max(pr_item[3], now_item[3])
            else:
                new_cuts.append(now_item)
                pr_k += 1
        cuts = new_cuts
    return cuts

# 获取图像中的各个小分割图像的函数，它可以以数据的形式返回，也可以将之以图像的形式保存到磁盘
# image代表着带分割图像；dir则是图像保存的目的路径
# is_data表示image是灰度值矩阵还是一个文件名；n_lines表示分割图像中符号的行数
# data_needed是表示是否需要以数据的形式返回图像的数据集；count是为了方便统计分割符号数量的一个parameter，可忽略
def get_image_cuts(image, dir=None, is_data=False, n_lines=1, data_needed=False, count=0):
    if is_data:
        data = image
    else:
        # 灰度处理
        data = cv2.imread(image, 2)
        # 获得坐标范围
    cuts = get_x_y_cuts(data, n_lines=n_lines)
    image_cuts = None
    for i, item in enumerate(cuts):
        count += 1
        max_dim = max(item[1] - item[0], item[3] - item[2])
        new_data = np.ones((int(1.4 * max_dim), int(1.4 * max_dim))) * 255
        x_min, x_max = (max_dim - item[1] + item[0]) // 2, (max_dim - item[1] + item[0]) // 2 + item[1] - item[0]
        y_min, y_max = (max_dim - item[3] + item[2]) // 2, (max_dim - item[3] + item[2]) // 2 + item[3] - item[2]
        new_data[int(0.2 * max_dim) + x_min:int(0.2 * max_dim) + x_max, int(0.2 * max_dim) + y_min:int(0.2 * max_dim) + y_max] = data[item[0]:item[1], item[2]:item[3]]
        standard_data = cv2.resize(new_data, (28, 28))
        if not data_needed:
            cv2.imwrite(dir + str(count) + ".jpg", standard_data)
        if data_needed:
            data_flat = (255 - np.resize(standard_data, (1, 28 * 28))) / 255
            if image_cuts is None:
                image_cuts = data_flat
            else:
                image_cuts = np.r_[image_cuts, data_flat]
    if data_needed:
        return image_cuts
    return count
# 获得新数据集的图像和标签
def get_images_labels():
    images = None
    labels = None
    pickle_images = open('../data/images', 'rb')
    pickle_labels = open('../data/labels', 'rb')
    images = pickle.load(pickle_images)
    labels = pickle.load(pickle_labels)
    pickle_images.close()
    pickle_labels.close()
    return images, labels