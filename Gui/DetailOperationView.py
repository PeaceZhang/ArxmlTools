from PySide6.QtWidgets import QWidget, QHBoxLayout, QToolBar, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QActionGroup, QIcon

class DOV:
    def __init__(self):
        self.view = DOV_VIEW()
        self.data = DOV_DATA()
        pass

class DOV_VIEW(QWidget):
    def __init__(self):
        super().__init__()

        toolbar = QToolBar('View')
        toolbar.setOrientation(Qt.Vertical)

        action_group = QActionGroup(self)
        action_group.setExclusive(True)

        # 添加一些动作按钮到工具栏
        action1 = QAction("Function View", self)
        action1.setCheckable(True)
        action1.setActionGroup(action_group)
        action1.setIcon(QIcon("Icon/functionview.png"))

        action2 = QAction("Interactive View", self)
        action2.setCheckable(True)
        action2.setActionGroup(action_group)
        action2.setIcon(QIcon("Icon/interactive.png"))

        action3 = QAction("PIM View", self)
        action3.setCheckable(True)
        action3.setActionGroup(action_group)
        action3.setIcon(QIcon("Icon/pimview.png"))

        action4 = QAction("Structure View", self)
        action4.setCheckable(True)
        action4.setActionGroup(action_group)
        action4.setIcon(QIcon("Icon/structureview.png"))

        action5 = QAction("OutSide View", self)
        action5.setCheckable(True)
        action5.setActionGroup(action_group)
        action5.setIcon(QIcon("Icon/outsideview.png"))

        toolbar.addAction(action1)
        toolbar.addAction(action2)
        toolbar.addAction(action3)
        toolbar.addAction(action4)
        toolbar.addAction(action5)

        layout = QHBoxLayout(self)
        layout.addWidget(toolbar)
        layout.addWidget(QTextEdit())
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        pass

class DOV_DATA:
    def __init__(self):
        pass