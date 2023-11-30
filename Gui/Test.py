from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
import sys

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建标签页窗口
        tab_widget = QTabWidget(self)
        self.setCentralWidget(tab_widget)

        # 创建两个标签页
        tab1 = QWidget()
        tab2 = QWidget()

        # 将标签页添加到标签控件
        tab_widget.addTab(tab1, "Tab 1")
        tab_widget.addTab(tab2, "Tab 2")

        # 设置标签页样式
        # tab_widget.setStyleSheet("""
        #     QTabWidget::pane { /* 整体样式 */
        #         border: 2px solid #C0C0C0;
        #         background-color: #F0F0F0;
        #     }
        #
        #     QTabBar::tab { /* 单个标签的样式 */
        #         background-color: #D0D0D0;
        #         border: 1px solid #C0C0C0;
        #         border-bottom-color: #A0A0A0;
        #         min-width: 8ex;
        #         padding: 3px;
        #     }
        #
        #     QTabBar::tab:selected { /* 选中的标签样式 */
        #         background-color: #E0E0E0;
        #     }
        #
        #     QTabBar::tab:!selected { /* 未选中的标签样式 */
        #         margin-top: 2px; /* 上边距 */
        #     }
        # """)

def main():
    app = QApplication(sys.argv)

    # 创建主窗口对象
    my_window = MyMainWindow()
    my_window.show()

    # 运行应用程序
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
