from osgeo import gdal

def get_nodata_value(tif_path):
    dataset = gdal.Open(tif_path)
    if not dataset:
        raise FileNotFoundError(f"无法打开文件：{tif_path}")

    nodata_values = []
    for band_index in range(1, dataset.RasterCount + 1):
        band = dataset.GetRasterBand(band_index)
        nodata = band.GetNoDataValue()
        nodata_values.append(nodata)

    return nodata_values


file_path = r"D:\BaiduNetdiskDownload\日本横须贺市-1米影像图.tif"
nodata_list = get_nodata_value(file_path)
print("每个波段的无效值为：", nodata_list)
