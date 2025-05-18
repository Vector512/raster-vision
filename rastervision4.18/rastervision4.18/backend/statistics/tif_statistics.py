import os
import numpy as np
from osgeo import gdal

def compute_band_statistics_with_histogram(file_path):
    dataset = gdal.Open(file_path)
    if not dataset:
        raise FileNotFoundError(f"无法打开文件进行统计：{file_path}")

    stats_data = []
    histogram_data = []

    for i in range(1, dataset.RasterCount + 1):
        band = dataset.GetRasterBand(i)
        nodata_value = band.GetNoDataValue()
        array = band.ReadAsArray()

        # 若存在无效值，则掩膜处理
        if nodata_value is not None:
            array = np.ma.masked_equal(array, nodata_value)
        else:
            array = np.ma.masked_invalid(array)

        # 计算统计量（跳过掩膜值）
        min_val = float(array.min())
        max_val = float(array.max())
        mean_val = float(array.mean())
        std_val = float(array.std())
        stats_data.append((f"波段 {i}", min_val, max_val, mean_val, std_val))

        # 构建直方图（排除无效值）
        valid_data = array.compressed()  # 去除掩膜值
        hist, _ = np.histogram(valid_data, bins=np.arange(257))  # DN 0~255
        total_pixels = hist.sum()
        cumulative = np.cumsum(hist)
        percentage = hist / total_pixels * 100
        cumulative_percentage = cumulative / total_pixels * 100

        band_hist_info = []
        for dn in range(256):
            count = hist[dn]
            if count > 0:
                band_hist_info.append((
                    dn,
                    int(count),
                    int(cumulative[dn]),
                    float(percentage[dn]),
                    float(cumulative_percentage[dn])
                ))

        histogram_data.append(band_hist_info)

    file_name = os.path.basename(file_path)
    return stats_data, histogram_data, file_name
