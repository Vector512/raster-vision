from osgeo import gdal
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import Qt

def process_tif_file(file_path):
    """
    处理 TIF 文件，返回文件节点和其波段子节点（用于添加到 TreeView）
    :param file_path: TIF 文件路径
    :return: file_item（QStandardItem），或 None 表示处理失败
    """
    dataset = gdal.Open(file_path)
    if not dataset:
        return None  # 控制器再决定怎么处理失败情况

    num_bands = dataset.RasterCount
    file_item = QStandardItem(file_path.split('/')[-1])  # 显示文件名
    file_item.setData(file_path, Qt.UserRole)  # 存路径

    for i in range(1, num_bands + 1):
        band_item = QStandardItem(f"波段 {i}")
        file_item.appendRow(band_item)

    return file_item
