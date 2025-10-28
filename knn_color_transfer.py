import numpy as np
from matplotlib import pyplot as plt
from skimage.color import rgb2lab, lab2rgb
from sklearn.neighbors import KNeighborsRegressor

from refactor import deal

block_size = 1


def color_transfer(content, style):
    print()
    try:
        handled_content, handled_style = deal(content, style)
    except Exception as e:
        print('deal()')

    knn = define_knn(4)
    try:
        X, Y = read_style_img(handled_style)
    except Exception as e:
        print('read_style_img()')

    knn.fit(X, Y)
    try:
        photo = rebuild(handled_content, knn)
    except Exception as e:
        print('rebuild()')

    # 为了展示图像，我们将其再转换为RGB表示
    new_photo = lab2rgb(photo)
    return new_photo
    # plt.show()


def read_style_img(img, size=block_size):

    # convert img from RGB to LAB
    img = rgb2lab(img)
    # get w, h  (img 为w * h * 3)
    w, h = img.shape[:2]

    # X 存储windows的灰度（light）
    # Y 存储中心中心像素色彩值
    X = []
    Y = []

    # 遍历每个中心像素 以及window
    # 这里已经resize ，都是256x256 的image
    for x in range(size, w - size):
        for y in range(size, h - size):
            # X.shape = [?, 9]
            X.append(img[x - size : x + size + 1, y - size: y + size + 1, 0].flatten())
            # Y.shape = [?, 2]
            Y.append(img[x, y, 1:])
    return X, Y


def rebuild(img, knn, size=block_size):
    # convert img from RGB to LAB
    img = rgb2lab(img)
    # get w, h  (img 为w * h * 3)
    w, h = img.shape[:2]

    # 初始化输出图像对应的矩阵
    photo = np.zeros_like(img)
    # 枚举内容图像的中心点，保存所有windows
    print('Constructing window...')

    X = []
    for x in range(size, w - size):
        for y in range(size, w - size):
            window = img[x - size: x + size + 1, y - size: y + size + 1, 0].flatten()
            X.append(window)

    X = np.array(X)
    # 用KNN回归器预测颜色
    print('Predicting...')

    # pred_ab.shape = Y.shape
    pred_ab = knn.predict(X).reshape(w - 2 * size, h - 2 * size, -1)
    # 设置输出图像
    photo[:, :, 0] = img[:, :, 0]
    photo[size: w - size, size: h - size, 1:] = pred_ab

    # 由于最外面size层无法构造窗口，简单起见，我们直接把这些像素裁剪掉
    photo = photo[size: w - size, size: h - size, :]
    return photo


def define_knn(k):
    knn = KNeighborsRegressor(n_neighbors=k, weights='distance')
    return knn
