from PySide6.QtWidgets import QTreeView, QFileSystemModel


class FileExplorer(QTreeView):
    def __init__(self):
        super().__init__()
        # 使用 QFileSystemModel 作为数据模型，显示文件系统结构
        model = QFileSystemModel()
        model.setRootPath("/")
        # 设置模型
        self.setModel(model)
        self.setRootIndex(model.index("/"))  # 设置根目录

