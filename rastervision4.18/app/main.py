import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR) # 项目根目录加到sys.path,否则frontend导入不了

from PyQt5.QtWidgets import QApplication
from frontend.main_window import Window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Window()
    main_window.show()
    sys.exit(app.exec_())