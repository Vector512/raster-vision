# GraphicsView的提升控件，用以实现用鼠标滚轮滚动放缩图像的功能。

# 在 Qt Designer 中，Promote to...（提升控件）是一种 将现有控件替换为自定义控件的机制。
# 它允许你在UI设计时使用标准控件（如 QGraphicsView、QPushButton 等），
# 然后在运行时将这些控件替换为你自己定义的子类，从而在保留UI设计的前提下，实现更复杂的自定义行为
# 简而言之，就是给GraphicsView类下添加一个子类，实现滚轮放缩的功能。


from PyQt5.QtWidgets import QGraphicsView

class ZoomableGraphicsView(QGraphicsView):
    def __init__(self,zoom_label,parent=None):
        super().__init__(parent)
        self.zoom_label = zoom_label
        self.scale_factor = 1.15  # 缩放因子
        self.min_zoom = 0.02       # 最小缩放
        self.max_zoom = 200.0       # 最大缩放
        self.current_zoom = 1.0   # 当前缩放倍数


    def wheelEvent(self, event):
        """监听鼠标滚轮事件，实现放大/缩小"""
        if event.angleDelta().y() > 0:  # 滚轮向上 -> 放大
            if self.current_zoom < self.max_zoom:
                self.scale(self.scale_factor, self.scale_factor)
                self.current_zoom *= self.scale_factor
        else:  # 滚轮向下 -> 缩小
            if self.current_zoom > self.min_zoom:
                self.scale(1 / self.scale_factor, 1 / self.scale_factor)
                self.current_zoom /= self.scale_factor
