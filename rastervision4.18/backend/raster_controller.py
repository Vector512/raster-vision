import os
from PyQt5.QtWidgets import QGraphicsScene, QMessageBox
from PyQt5.QtCore import Qt
from backend.utils.stretch_method import stretch_linear, stretch_linear_pct1
from frontend.views.stretch_image_window import StretchImageWindow
from osgeo import gdal
import numpy as np

class RasterController:
    def __init__(self, window):
        self.window = window
        self.scene = QGraphicsScene(self.window)
        self.window.graphicsView.setScene(self.scene)
        self.tree_model = self.window.tree_model  # 获取树形控件
        self.treeView = self.window.treeView  # 获取 treeView 控件
    
    def open_file(self, file_path):
        extension = os.path.splitext(file_path)[1].lower()  # 获取文件扩展名并转为小写
        if extension in [".tif", ".tiff"]:
            self.display_original_image(file_path)  # 这里传递掩膜信息
            self.load_file_to_tree(file_path)  # 载入文件到树
            self.show_crs_info(file_path)  # 显示坐标系信息
            return True
        elif extension == ".pdf":
            # TODO: 加载 PDF 文件的展示逻辑
            # self.load_pdf_to_tree(file_path)
            # self.display_pdf_image(file_path)
            # self.show_crs_info(file_path)
            QMessageBox.information(self.window, "尚未实现", "PDF 文件的支持尚在开发中。")
            return False
        elif extension == ".png":
            # TODO: 加载 PNG 文件的展示逻辑
            # self.load_png_to_tree(file_path)
            # self.display_png_image(file_path)
            # self.show_crs_info(file_path)
            QMessageBox.information(self.window, "尚未实现", "PNG 文件的支持尚在开发中。")
            return False
        elif extension == ".img":
            # TODO: 加载 ERDAS .img 文件
            # self.load_img_to_tree(file_path)
            # self.display_img_image(file_path)
            # self.show_crs_info(file_path)
            QMessageBox.information(self.window, "尚未实现", ".img 文件的支持尚在开发中。")
            return False
        elif extension in [".hdf", ".hdf5"]:
            # TODO: 加载 HDF 文件的逻辑（如 MODIS 数据）
            # self.load_hdf_to_tree(file_path)
            # self.display_hdf_image(file_path)
            # self.show_crs_info(file_path)
            QMessageBox.information(self.window, "尚未实现", "HDF 文件的支持尚在开发中。")
            return False
        else:
            QMessageBox.warning(self.window, "格式不支持", f"暂不支持该格式的文件：{extension}")
            return False

    def load_file_to_tree(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        # 判断文件格式，并进行相应的处理
        if ext in ('.tif', '.tiff'):
            from backend.create_file_tree.tif_tree import process_tif_file
            file_item = process_tif_file(file_path)
        else:
            self.show_message("文件类型不支持", f"{ext} 格式暂不支持", QMessageBox.Critical)
            return

        if file_item is None:
            self.show_message("文件读取失败", "无法处理该文件", QMessageBox.Critical)
            return

        self.tree_model.appendRow(file_item)
        self.window.treeView.expandAll()

    def display_original_image(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ('.tif', '.tiff'):
            from backend.display_image.display_tif_image import display_original_image, configure_graphics_view
            display_original_image(self.scene, file_path)
            configure_graphics_view(self.window.graphicsView)
        elif ext == '.png':
            # TODO: 加载 PNG 文件图像
            # from backend.display_image.display_png_image import display_png_image
            # display_png_image(self.scene, file_path)
            QMessageBox.information(self.window, "尚未实现", "PNG 文件的显示功能尚未开发。")
        elif ext == '.pdf':
            # TODO: 加载 PDF 文件图像
            # from backend.display_image.display_pdf_image import display_pdf_image
            # display_pdf_image(self.scene, file_path)
            QMessageBox.information(self.window, "尚未实现", "PDF 文件的显示功能尚未开发。")
        elif ext == '.img':
            # TODO: 加载 IMG 文件图像
            # from backend.display_image.display_img_image import display_img_image
            # display_img_image(self.scene, file_path)
            QMessageBox.information(self.window, "尚未实现", ".img 文件的显示功能尚未开发。")
        elif ext in ('.hdf', '.hdf5'):
            # TODO: 加载 HDF 文件图像
            # from backend.display_image.display_hdf_image import display_hdf_image
            # display_hdf_image(self.scene, file_path)
            QMessageBox.information(self.window, "尚未实现", "HDF 文件的显示功能尚未开发。")
        else:
            QMessageBox.warning(self.window, "格式不支持", f"暂不支持该格式的图像显示：{ext}")

    def display_band(self, file_path, band_index):
        ext = os.path.splitext(file_path)[1].lower()

        if ext in ('.tif', '.tiff'):
            from backend.display_image.display_tif_image import display_band ,configure_graphics_view
            display_band(self.scene, file_path, band_index)
            configure_graphics_view(self.window.graphicsView)
        elif ext == '.img':
            # TODO: 显示 IMG 文件指定波段
            # from backend.display_image.display_img_image import display_band as display_img_band
            # display_img_band(self.scene, file_path, band_index)
            QMessageBox.information(self.window, "尚未实现", ".img 文件波段显示功能尚未开发。")
        elif ext in ('.hdf', '.hdf5'):
            # TODO: 显示 HDF 文件指定波段
            # from backend.display_image.display_hdf_image import display_band as display_hdf_band
            # display_hdf_band(self.scene, file_path, band_index)
            QMessageBox.information(self.window, "尚未实现", "HDF 文件波段显示功能尚未开发。")
        else:
            QMessageBox.warning(self.window, "格式不支持", f"暂不支持该格式的波段显示：{ext}")

    def get_file_path_from_tree_model(self, tree_model, file_name):
        """
        根据文件名在 tree_model 中查找对应的完整文件路径。
        """
        for i in range(tree_model.rowCount()):
            root_item = tree_model.item(i)
            if root_item.text() == file_name:
                return root_item.data(Qt.UserRole)
        return None

    def handle_tree_item_click(self,index):
        """
        响应树状图中点击事件，根据点击的内容（文件或波段）进行图像显示与 CRS 信息更新。
        """
        item = self.tree_model.itemFromIndex(index)
        parent = item.parent()
        if parent is None:
            # 点击的是文件节点
            file_name = item.text()
            for i in range(self.tree_model.rowCount()):
                root_item = self.tree_model.item(i)
                if root_item.text() == file_name:
                    file_path = root_item.data(Qt.UserRole)
                    extension = os.path.splitext(file_path)[1].lower()
                    self.window.current_file_path = file_path  # 把文件路径赋值给 current_file_path
                    if extension in ['.tif', '.tiff']:
                        self.display_original_image(file_path)
                        self.show_crs_info(file_path)
                    elif extension == '.pdf':
                        # 预留接口：显示PDF（如支持地图扫描件等）
                        pass
                    elif extension == '.png':
                        # 预留接口：显示PNG图像
                        pass
                    elif extension == '.img':
                        # 预留接口：ERDAS IMAGINE 格式
                        pass
                    elif extension in ['.hdf', '.hdf5']:
                        # 预留接口：HDF 格式图像
                        pass
                    else:
                        self.window.show_message("提示", f"暂不支持该格式：{extension}", QMessageBox.Warning)
                    break
        else:
            # 点击的是波段节点
            band_text = item.text()
            band_index = int(band_text.split()[-1])  # 从"波段 1"中提取索引
            file_item = parent
            file_name = file_item.text()
            for i in range(self.tree_model.rowCount()):
                root_item = self.tree_model.item(i)
                if root_item.text() == file_name:
                    file_path = root_item.data(Qt.UserRole)
                    self.window.current_file_path = file_path  # 把文件路径赋值给 current_file_path
                    extension = os.path.splitext(file_path)[1].lower()

                    if extension in ['.tif', '.tiff']:
                        self.display_band(file_path, band_index)
                        self.show_crs_info(file_path)
                    elif extension == '.img':
                        # 预留：处理 .img 的单波段显示
                        pass
                    elif extension in ['.hdf', '.hdf5']:
                        # 预留：处理 HDF 格式单波段
                        pass
                    else:
                        self.window.show_message("提示", f"暂不支持该格式的波段查看：{extension}", QMessageBox.Warning)
                    break

    def show_crs_info(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ('.tif', '.tiff'):
            from backend.show_crs_info.show_tif_crs_info import show_tif_crs_info
            crs_info = show_tif_crs_info(file_path)
            self.window.label_crs.setText(crs_info)
        elif ext == '.pdf':
            pass
        elif ext == '.png':
            pass
        elif ext == '.img':
            pass
        elif ext in ('.hdf', '.hdf5'):
            pass
        else:
            self.window.label_crs.setText("不支持的格式")

    def save_image(self, file_path):
        """保存当前显示的图像到指定路径"""
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ('.tif', '.tiff'):
            from backend.display_image.display_tif_image import save_tif_image
            save_tif_image(self.scene, self.window, file_path)
        elif ext == '.png':
            # TODO: 保存为 PNG 图像
            # from backend.display_image.display_png_image import save_png_image
            # save_png_image(self.scene, self.window, file_path)
            QMessageBox.information(self.window, "尚未实现", ".png 图像保存功能尚未开发。")
        elif ext == '.pdf':
            # TODO: 保存为 PDF 图像
            # from backend.display_image.display_pdf_image import save_pdf_image
            # save_pdf_image(self.scene, self.window, file_path)
            QMessageBox.information(self.window, "尚未实现", ".pdf 图像保存功能尚未开发。")
        elif ext == '.img':
            # TODO: 保存为 .img 图像
            QMessageBox.information(self.window, "尚未实现", ".img 图像保存功能尚未开发。")
        elif ext in ('.hdf', '.hdf5'):
            # TODO: 保存为 .hdf 图像
            QMessageBox.information(self.window, "尚未实现", ".hdf 图像保存功能尚未开发。")
        else:
            QMessageBox.warning(self.window, "格式不支持", f"暂不支持该格式的图像保存：{ext}")


    def quick_statistics(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()

        try:
            if ext in ('.tif', '.tiff'):
                from backend.statistics.tif_statistics import compute_band_statistics_with_histogram
                return compute_band_statistics_with_histogram(file_path)
            elif ext == '.img':
                # TODO: 添加对 .img 文件的波段统计
                self.window.show_message("提示", "暂未实现 .img 文件的波段统计")
                return None, None, ""
            elif ext in ('.hdf', '.hdf5'):
                # TODO: 添加对 .hdf 文件的波段统计
                self.window.show_message("提示", "暂未实现 .hdf 文件的波段统计")
                return None, None, ""
            else:
                self.window.show_message("格式不支持", f"暂不支持该格式的波段统计：{ext}")
                return None, None, ""
        except Exception as e:
            self.window.show_message("错误", f"统计失败：{e}")
            return None, None, ""
    
    def handle_right_click_action(self, action_type, file_path):
        if action_type == "quick_statistics":
            try:
                from backend.statistics.tif_statistics import compute_band_statistics_with_histogram
                stats_data, histogram_data, file_name = compute_band_statistics_with_histogram(file_path)
                if stats_data and histogram_data:
                    from frontend.views.stats_viewer import show_statistics_window
                    show_statistics_window(stats_data, histogram_data, file_name)
            except Exception as e:
                self.window.show_message("错误", f"统计失败：{e}", QMessageBox.Critical)
        # 后续可扩展其他右键功能
        elif action_type == "open_attribute_table":
            pass
        elif action_type == "export_metadata":
            pass

    def apply_stretch_mode(self, file_path, mode):
        print(f"[控制器] 拉伸模式：{mode}，文件路径：{file_path}")

        dataset = gdal.Open(file_path)
        if dataset is None:
            print("[控制器] 无法打开文件")
            return

        band_count = dataset.RasterCount
        print(f"[控制器] 波段数：{band_count}")

        stretch_functions = {
            "linear": stretch_linear,
            "linear_pct1": stretch_linear_pct1,  # 新增的拉伸模式
            # 后续可以扩展其他模式，如：'log'、'equalize'、'sqrt'等
        }

        stretch_func = stretch_functions.get(mode)
        if not stretch_func:
            print(f"[控制器] 未找到拉伸模式：{mode}")
            return

        if band_count >= 3:
            # 多波段彩色图像（使用前3个波段）
            rgb_array = []
            combined_mask = None

            for i in range(1, 4):  # 读取第1-3波段
                band = dataset.GetRasterBand(i)
                arr = band.ReadAsArray()
                no_data_value = band.GetNoDataValue()
                if arr is None:
                    print(f"[控制器] 无法读取第{i}个波段")
                    return
                if no_data_value is not None:
                    print(f"[控制器] 第{i}波段检测到无效值：{no_data_value}")
                    band_mask = (arr == no_data_value)
                    combined_mask = band_mask if combined_mask is None else (combined_mask | band_mask)

                rgb_array.append(arr)

            # 应用统一掩膜（如果存在）
            if combined_mask is not None:
                rgb_array = [np.ma.array(band_arr, mask=combined_mask, copy=False) for band_arr in rgb_array]

            # 分别对每个波段应用拉伸
            print(f"[控制器] 应用拉伸模式：{mode}")
            stretched_bands = [stretch_func(band_arr) for band_arr in rgb_array]

            # 合并为RGB图像
            stretched_rgb = np.stack(stretched_bands, axis=-1)  # shape: (H, W, 3)
            print(f"[控制器] 彩色图像拉伸完成，准备显示")

            # 显示窗口
            self.stretch_window = StretchImageWindow()
            self.stretch_window.display_image(stretched_rgb)

        else:
            # 单波段图像
            band = dataset.GetRasterBand(1)
            array = band.ReadAsArray()

            if array is None:
                print("[控制器] 无法读取图像数据")
                return

            no_data_value = band.GetNoDataValue()
            if no_data_value is not None:
                print(f"[控制器] 检测到无效值：{no_data_value}")
                array = np.ma.masked_equal(array, no_data_value)

            print(f"[控制器] 应用拉伸模式：{mode}")
            stretched = stretch_func(array)
            print(f"[控制器] 单波段图像拉伸完成，准备显示")

            self.stretch_window = StretchImageWindow()
            self.stretch_window.display_image(stretched)

    def show_message(self, title, message, icon_type):
        """弹出消息框显示信息"""
        msg_box = QMessageBox(self.window)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon_type)
        msg_box.exec_()


