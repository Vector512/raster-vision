# frontend/views/stats_viewer.py
import mplcursors
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QTabWidget, QSizePolicy, QSplitter
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# 设置中文字体支持
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
matplotlib.rcParams['axes.unicode_minus'] = False    # 解决负号显示为方块的问题

_statistics_window_instance = None

class StatisticsWindow(QWidget):
    def __init__(self, stats_data, histogram_data, file_name):
        super().__init__()
        self.setWindowTitle(f"{file_name} - 波段统计信息")
        self.setMinimumSize(1000, 700)

        # 顶级垂直分割器：上为基础信息表格，下为各波段tab
        splitter_main = QSplitter(Qt.Vertical)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(splitter_main)

        # 总览表格：波段最小值、最大值、均值、标准差
        self.table = QTableWidget(len(stats_data), 5)
        self.table.setHorizontalHeaderLabels(["波段", "最小值", "最大值", "均值", "标准差"])

        for row, (band_name, min_val, max_val, mean, std_dev) in enumerate(stats_data):
            self.table.setItem(row, 0, QTableWidgetItem(str(band_name)))
            self.table.setItem(row, 1, QTableWidgetItem(f"{min_val:.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(f"{max_val:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{mean:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{std_dev:.2f}"))

        self.table.resizeColumnsToContents()
        splitter_main.addWidget(self.table)

        # Tab 每个波段一页
        self.tabs = QTabWidget()
        splitter_main.addWidget(self.tabs)

        # 设置分割比例：基础信息 1/4，高度比例为 1:3
        splitter_main.setStretchFactor(0, 1)
        splitter_main.setStretchFactor(1, 3)

        for idx, band_hist in enumerate(histogram_data):
            self.add_band_tab(idx + 1, band_hist)

    def add_band_tab(self, band_index, band_hist):
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)

        # 使用左右分割：左是表格，右是直方图
        splitter = QSplitter(Qt.Horizontal)

        # 1. 表格
        hist_table = QTableWidget(len(band_hist), 5)
        hist_table.setHorizontalHeaderLabels(["DN值", "数量", "累计数量", "百分比%", "累计百分比%"])

        for row, (dn, count, cum_count, percent, cum_percent) in enumerate(band_hist):
            hist_table.setItem(row, 0, QTableWidgetItem(str(dn)))
            hist_table.setItem(row, 1, QTableWidgetItem(str(count)))
            hist_table.setItem(row, 2, QTableWidgetItem(str(cum_count)))
            hist_table.setItem(row, 3, QTableWidgetItem(f"{percent:.2f}"))
            hist_table.setItem(row, 4, QTableWidgetItem(f"{cum_percent:.2f}"))

        hist_table.resizeColumnsToContents()
        splitter.addWidget(hist_table)

        # 2. 曲线图（右边）
        fig = Figure(figsize=(4, 3))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        # 获取 DN 值和数量
        dn_values = [item[0] for item in band_hist]
        counts = [item[1] for item in band_hist]
        # 绘制曲线图
        ax.plot(dn_values, counts, color='skyblue', linewidth=1.2)  
        ax.fill_between(dn_values, counts, color='skyblue', alpha=0.3)  # 填充曲线下方区域
        # 设置标题和轴标签
        ax.set_title(f"波段 {band_index} 像元值分布", fontsize=22)
        ax.set_xlabel("DN 值", fontsize=18)
        ax.set_ylabel("数量", fontsize=18)
        # 确保纵轴从0开始
        ax.set_ylim(bottom=0)

        # 启用鼠标悬停显示信息，并确保每个点只显示一个DN值和整数数量
        mplcursors.cursor(ax, hover=True).connect("add", lambda sel: sel.annotation.set_text(
            f"X: {int(sel.target[0])}\nY: {int(sel.target[1])}"))  # 显示整数数量

        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas.updateGeometry()
        splitter.addWidget(canvas)

        # 设置左右比例：表格 2，图像 3（可自由调整）
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)

        tab_layout.addWidget(splitter)
        self.tabs.addTab(tab, f"波段 {band_index}")

def show_statistics_window(stats_data, histogram_data, file_name):
    global _statistics_window_instance
    _statistics_window_instance = StatisticsWindow(stats_data, histogram_data, file_name)
    _statistics_window_instance.show()

# show_statistics_window是类的使用逻辑，而StatisticsWindow是统计窗口ui的显示逻辑
# StatisticsWindow封装统计窗口的界面结构和展示逻辑，比如表格、直方图、窗口标题等等
# show_statistics_window封装窗口的创建与展示动作，便于在控制器或者其他前端逻辑中直接调用