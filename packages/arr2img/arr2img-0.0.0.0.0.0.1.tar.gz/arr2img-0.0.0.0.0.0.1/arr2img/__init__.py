#! python
# @Time    : 23/08/04 上午 10:36
# @Author  : azzhu 
# @FileName: __init__.py.py
# @Software: PyCharm
import numpy as np

__version__ = '0.0.0.0.0.0.1'


def arr2img(
        a,
        min2zero=True,  # 图像最小值是否从0开始
        deep=16,  # 位深度，可选8,16
        enhance=1,  # 亮度增强倍数

):
    # 拷贝一份，不改变原始数据
    img = a.copy().astype(float)

    # 如最小值小于0或者强制要求最小值为0，一定要减去最小值
    if img.min() < 0 or min2zero:
        img -= img.min()

    # 根据位深度设定相关参数
    if deep == 8 or deep == 16:
        maxv = 2 ** deep - 1
        dtype = np.uint8 if deep == 8 else np.uint16
    else:
        raise ValueError

    # 调整矩阵取值范围
    img /= img.max()
    img *= maxv

    # 亮度增强
    if enhance > 1:
        img *= enhance
        img = np.clip(img, 0, maxv)

    # 四舍五入取整
    img = np.round(img).astype(dtype)

    # 彩色通道如果不在最后则移到最后
    sp = img.shape
    if len(sp) == 3:
        if sp[0] == 3:
            img = np.transpose(img, [1, 2, 0])
        if sp[1] == 3:
            img = np.transpose(img, [0, 2, 1])

    return img
