from PyQt5.QtWidgets import QMessageBox, QGraphicsPixmapItem

def save_tif_image(scene, window, file_path):
    """保存当前显示的图像到指定路径"""
    if not scene.items():
        QMessageBox.warning(window, "保存失败", "没有图像可以保存！")
        return

    item = scene.items()[0]  # 假设只有一个图像项
    if isinstance(item, QGraphicsPixmapItem):
        pixmap = item.pixmap()
        if pixmap.save(file_path):
            QMessageBox.information(window, "保存成功", f"文件已保存到: {file_path}")
        else:
            QMessageBox.critical(window, "保存失败", "文件保存失败！")
    else:
        QMessageBox.critical(window, "保存失败", "当前图像格式无法保存！")
