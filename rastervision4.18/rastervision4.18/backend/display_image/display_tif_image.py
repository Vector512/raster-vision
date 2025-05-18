from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPainter
from osgeo import gdal

def display_original_image(scene, file_path):
    """
    显示原图
    :param scene: QGraphicsScene 实例
    :param file_path: 图像文件路径
    """
    pixmap = QPixmap(file_path)
    if not pixmap.isNull():
        scene.clear()
        item = QGraphicsPixmapItem(pixmap)
        item.setFlag(QGraphicsPixmapItem.ItemIsMovable)
        scene.addItem(item)

def display_band(scene, file_path, band_index):
    """
    显示单一波段图像
    :param scene: QGraphicsScene 实例
    :param file_path: 图像文件路径
    :param band_index: 波段索引（1-based）
    """
    dataset = gdal.Open(file_path)
    if not dataset:
        raise ValueError("无法读取文件")

    band = dataset.GetRasterBand(band_index)
    data = band.ReadAsArray()

    # 归一化到 0-255
    norm_data = ((data - data.min()) / (data.ptp() + 1e-6) * 255).astype('uint8')

    height, width = norm_data.shape
    image = QImage(norm_data.data, width, height, norm_data.strides[0], QImage.Format_Grayscale8)
    pixmap = QPixmap.fromImage(image)

    scene.clear()
    item = QGraphicsPixmapItem(pixmap)
    item.setFlag(QGraphicsPixmapItem.ItemIsMovable)
    scene.addItem(item)

def configure_graphics_view(graphics_view):
    """
    配置图像展示的渲染设置
    :param graphics_view: QGraphicsView 实例
    """
    graphics_view.setRenderHint(QPainter.Antialiasing)
    graphics_view.setRenderHint(QPainter.SmoothPixmapTransform)
