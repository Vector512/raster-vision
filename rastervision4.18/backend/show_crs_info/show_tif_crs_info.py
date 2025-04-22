from osgeo import gdal, osr

def show_tif_crs_info(file_path):
    """
    处理TIF文件的坐标系统信息
    :param file_path: TIF文件路径
    :return: 坐标系统信息字符串
    """
    dataset = gdal.Open(file_path)
    if not dataset:
        return "无法读取坐标系统信息"

    proj = dataset.GetProjection()
    if not proj:
        return "该文件没有坐标系统信息"

    srs = osr.SpatialReference()
    srs.ImportFromWkt(proj)

    if srs.IsGeographic():
        crs_type = "地理坐标系"
    elif srs.IsProjected():
        crs_type = "投影坐标系"
    else:
        crs_type = "未知类型"

    name = srs.GetAttrValue("GEOGCS") or srs.GetAttrValue("PROJCS") or "未知名称"
    epsg = srs.GetAuthorityCode(None) or "未知EPSG"

    return f"{crs_type} | {name} | EPSG:{epsg}"
