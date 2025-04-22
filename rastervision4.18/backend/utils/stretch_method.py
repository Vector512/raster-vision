import numpy as np

def stretch_linear(array):
    """
    线性拉伸：将图像数据拉伸到 0~255 范围。
    输入可以是单波段 (2D) 或 RGB (3D)。
    """
    if array.ndim == 2:
        return _stretch_linear_2d(array)
    elif array.ndim == 3:
        stretched_bands = []
        for i in range(array.shape[2]):
            stretched = _stretch_linear_2d(array[:, :, i])
            stretched_bands.append(stretched)
        return np.stack(stretched_bands, axis=2)
    else:
        raise ValueError("Unsupported array shape for stretch_linear")

# backend/utils/stretch_method.py

def stretch_linear_pct1(array):
    """
    1%线性拉伸：将图像数据的最小值和最大值分别拉伸到1%和99%分位数。
    输入可以是单波段 (2D) 或 RGB (3D)。
    """
    if array.ndim == 2:
        return _stretch_linear_pct1_2d(array)
    elif array.ndim == 3:
        stretched_bands = []
        for i in range(array.shape[2]):
            stretched = _stretch_linear_pct1_2d(array[:, :, i])
            stretched_bands.append(stretched)
        return np.stack(stretched_bands, axis=2)
    else:
        raise ValueError("Unsupported array shape for stretch_linear_pct1")


def _stretch_linear_pct1_2d(array):
    """
    对单个波段图像进行1%线性拉伸。
    """

    # 保留掩膜，只对有效值计算百分位
    is_masked = isinstance(array, np.ma.MaskedArray)

    if is_masked:
        valid_data = array.compressed()  # 提取非掩膜部分
    else:
        valid_data = array


    min_val = np.percentile(valid_data, 1) # 获取图像1%的最小值
    max_val = np.percentile(valid_data, 99) # 获取图像99%的最大值

    # 拉伸计算（支持带掩膜）
    stretched = (array - min_val) / (max_val - min_val) * 255.0
    stretched = np.clip(stretched, 0, 255)

    # 转换为 uint8，保持掩膜
    stretched = stretched.astype(np.uint8)

    # 如果是掩膜数组，保持掩膜；否则直接返回
    return stretched if is_masked else stretched

def _stretch_linear_2d(array):
    """
    线性拉伸单个二维数组。
    """
    # array = ma.masked_invalid(array)
    min_val = array.min()
    max_val = array.max()

    if max_val == min_val:
        return np.zeros_like(array, dtype=np.uint8)

    stretched = (array - min_val) / (max_val - min_val) * 255
    return stretched.filled(0).astype(np.uint8)





# 可拓展：其他拉伸方法（等值、对数、平方根等）可在此添加
# def stretch_log(array):
#     pass

# def stretch_equalize(array):
#     pass

# def stretch_linear_percent(array, percent):
#     pass
