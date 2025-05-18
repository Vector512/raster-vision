from osgeo import gdal

def read_band_range(tif_file):
    # 打开TIF文件
    dataset = gdal.Open(tif_file)
    
    if not dataset:
        print(f"无法打开文件: {tif_file}")
        return

    # 获取波段数量
    band_count = dataset.RasterCount
    print(f"文件包含 {band_count} 个波段\n")

    # 遍历每个波段并输出其数值范围
    for band_idx in range(1, band_count + 1):
        band = dataset.GetRasterBand(band_idx)
        
        # 获取波段的统计信息
        min_value, max_value, _, _ = band.GetStatistics(True, True)
        
        print(f"波段 {band_idx} 的范围:")
        print(f"  最小值: {min_value}")
        print(f"  最大值: {max_value}")
        print('-' * 30)

# 输入TIF文件路径
tif_file_path = r"C:\Users\15852\Desktop\示例数据\三波段\广西.玉林.容县(2022.04).tif"  # 请替换为你自己的文件路径
read_band_range(tif_file_path)



