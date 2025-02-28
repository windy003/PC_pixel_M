import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor, QIcon

class PixelMeasureApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # 设置窗口标题和大小，添加版本信息
        self.setWindowTitle('屏幕像素测量工具 - 版本: 2025/2/28-01')
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建标签显示测量信息
        self.info_label = QLabel('点击并拖动鼠标来测量像素')
        self.info_label.setAlignment(Qt.AlignCenter)
        # 设置更大的字体
        font = self.info_label.font()
        font.setPointSize(14)
        self.info_label.setFont(font)
        layout.addWidget(self.info_label)
        
        # 创建测量结果标签
        self.result_label = QLabel('宽度: 0 像素, 高度: 0 像素, 对角线: 0 像素')
        self.result_label.setAlignment(Qt.AlignCenter)
        # 设置更大的字体
        self.result_label.setFont(font)
        layout.addWidget(self.result_label)
        
        # 初始化测量变量
        self.measuring = False
        self.start_point = QPoint()
        self.end_point = QPoint()
        
        # 设置窗口透明度
        self.setWindowOpacity(0.8)
        
        # 允许鼠标追踪
        self.setMouseTracking(True)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.measuring = True
            self.start_point = event.pos()
            self.end_point = event.pos()
            self.update()
    
    def mouseMoveEvent(self, event):
        if self.measuring:
            self.end_point = event.pos()
            self.updateMeasurement()
            self.update()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.measuring:
            self.measuring = False
            self.end_point = event.pos()
            self.updateMeasurement()
            self.update()
    
    def updateMeasurement(self):
        width = abs(self.end_point.x() - self.start_point.x())
        height = abs(self.end_point.y() - self.start_point.y())
        diagonal = int((width**2 + height**2)**0.5)
        
        self.result_label.setText(f'宽度: {width} 像素, 高度: {height} 像素, 对角线: {diagonal} 像素')
    
    def paintEvent(self, event):
        if self.measuring or (self.start_point != self.end_point):
            qp = QPainter(self)
            qp.setPen(QPen(QColor(255, 0, 0), 2, Qt.SolidLine))
            
            # 绘制矩形
            x = min(self.start_point.x(), self.end_point.x())
            y = min(self.start_point.y(), self.end_point.y())
            width = abs(self.end_point.x() - self.start_point.x())
            height = abs(self.end_point.y() - self.start_point.y())
            
            qp.drawRect(x, y, width, height)
            
            # 绘制对角线
            qp.setPen(QPen(QColor(0, 0, 255), 1, Qt.DashLine))
            qp.drawLine(self.start_point, self.end_point)

def main():
    app = QApplication(sys.argv)
    
    # 设置应用图标
    icon_path = get_resource_path("32x32.png")
    app.setWindowIcon(QIcon(icon_path))
    
    window = PixelMeasureApp()
    window.show()
    sys.exit(app.exec_())

# 处理资源路径，兼容PyInstaller打包后的情况
def get_resource_path(relative_path):
    """获取资源的绝对路径，兼容开发环境和PyInstaller打包后的环境"""
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        # 不是PyInstaller打包的情况，使用当前文件夹
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    main()
