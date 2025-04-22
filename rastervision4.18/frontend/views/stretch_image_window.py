# frontend/views/stretch_image_window.py

from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QPainter, QImage


class StretchImageWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("拉伸图像")

        # 创建 GraphicsView 和 Scene
        self.graphics_view = ZoomableGraphicsView(self)
        self.graphics_scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.graphics_scene)
        self.setCentralWidget(self.graphics_view)  # ✅ 设为中心控件

        self.setGeometry(100, 100, 800, 600)
        self.show()

    def display_image(self, image_array):
        """接收拉伸后的图像并显示"""
        # 判断图像是单通道还是三通道
        if image_array.ndim == 3:  # 彩色图像
            height, width, channels = image_array.shape
        else:  # 单通道图像
            height, width = image_array.shape
            channels = 1  # 设定通道为1

        # 将图像转换为QPixmap
        qimage = QImage(image_array.data, width, height, width * channels, QImage.Format_RGB888 if channels == 3 else QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimage)

        # 创建图像项并将其添加到场景
        pixmap_item = QGraphicsPixmapItem(pixmap)
        self.graphics_scene.clear()  # 清空之前的图像
        self.graphics_scene.addItem(pixmap_item)

        # 调整视图的大小适应图像
        self.graphics_view.setSceneRect(pixmap_item.boundingRect())
        self.graphics_view.setRenderHint(QPainter.Antialiasing)



class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

    def wheelEvent(self, event):
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor

        self.scale(zoom_factor, zoom_factor)


