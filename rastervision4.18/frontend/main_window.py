import os
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QFileDialog, QMenu, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt
from backend.raster_controller import RasterController  # 导入控制器类

# 获取当前脚本所在的目录
base_dir = os.path.dirname(os.path.abspath(__file__))
# 构建 UI 文件的绝对路径
ui_file = os.path.join(base_dir, "ui_design", "main_window.ui")
# 加载 UI 文件
FormClass, BaseClass = uic.loadUiType(ui_file)

class Window(BaseClass, FormClass):
    def __init__(self):
        super().__init__()
        self.tree_model = QStandardItemModel() # 创建一个标准的数据模型，用于存储树形结构的数据
        self.setupUi(self)
        self.current_file_path = None  # 初始化 current_file_path
        self.treeView.setModel(self.tree_model) # 将上面创建的数据模型绑定到树形控件 treeView 上
        self.treeView.header().hide()
        self.controller = RasterController(self)  # 将控制器绑定到视图

        # 绑定操作信号
        self.action_open.triggered.connect(self.on_open_file)
        self.action_save.triggered.connect(self.on_save_file)
        self.treeView.clicked.connect(self.on_tree_item_clicked)

        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)  # 创建上下文菜单
        self.treeView.customContextMenuRequested.connect(self.on_treeview_right_click) # 绑定槽函数

        self.action_stretch_linear.triggered.connect(self.on_stretch_linear)
        self.action_stretch_linear_pct1.triggered.connect(self.on_stretch_linear_pct1)
        self.action_stretch_linear_pct2.triggered.connect(self.on_stretch_linear_pct2)
        self.action_stretch_linear_pct5.triggered.connect(self.on_stretch_linear_pct5)


    def on_open_file(self):
        # 导入文件槽函数
        file_path, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "GeoTIFF 文件 (*.tif *.tiff);;所有文件 (*)")
        if file_path:
            success = self.controller.open_file(file_path)  # 调用控制器的方法
            if not success:
                return  # 如果文件格式不支持，直接返回

    def on_save_file(self):
        # 保存文件槽函数
        file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "GeoTIFF 文件 (*.tif *.tiff);;所有文件 (*)")
        if file_path:
            self.controller.save_image(file_path)  

    def on_tree_item_clicked(self, index):
        self.controller.handle_tree_item_click(index)

    def on_stretch_linear(self):
        """
        拉伸操作：应用线性拉伸
        """
        if hasattr(self, 'current_file_path') and self.current_file_path:
            file_path = self.current_file_path
            self.controller.apply_stretch_mode(file_path, "linear")  # 使用当前文件路径进行拉伸操作
        else:
            self.controller.show_message("提示", "请先选择一个文件进行拉伸", QMessageBox.Warning)
    
    def on_stretch_linear_pct1(self):
        """
        1% 线性拉伸槽函数
        """
        if hasattr(self, 'current_file_path') and self.current_file_path:
            file_path = self.current_file_path
            self.controller.apply_stretch_mode(file_path, "linear_pct1")  # 使用当前文件路径进行1%线性拉伸操作
        else:
            self.window.show_message("提示", "请先选择一个文件进行拉伸", QMessageBox.Warning)

    def on_stretch_linear_pct2(self):
        """
        2% 线性拉伸槽函数
        """
        if hasattr(self, 'current_file_path') and self.current_file_path:
            file_path = self.current_file_path
            self.controller.apply_stretch_mode(file_path, "linear_pct2")  # 使用当前文件路径进行2%线性拉伸操作
        else:
            self.window.show_message("提示", "请先选择一个文件进行拉伸", QMessageBox.Warning)

    def on_stretch_linear_pct5(self):
        """
        5% 线性拉伸槽函数
        """
        if hasattr(self, 'current_file_path') and self.current_file_path:
            file_path = self.current_file_path
            self.controller.apply_stretch_mode(file_path, "linear_pct5")  # 使用当前文件路径进行5%线性拉伸操作
        else:
            self.window.show_message("提示", "请先选择一个文件进行拉伸", QMessageBox.Warning)


    def on_treeview_right_click(self, pos):
        # UI 层仅处理视图和交互
        index = self.treeView.indexAt(pos)
        if not index.isValid():
            return

        item = self.tree_model.itemFromIndex(index)
        if item.parent() is not None:
            return  # 暂时只对文件右键

        file_path = item.data(Qt.UserRole)

        menu = QMenu(self)
        stats_action = menu.addAction("快速统计")
        action = menu.exec_(self.treeView.viewport().mapToGlobal(pos))

        if action == stats_action:
            self.controller.handle_right_click_action("quick_statistics", file_path)


