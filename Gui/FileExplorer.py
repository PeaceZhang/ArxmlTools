from PySide6.QtWidgets import QTreeView, QFileSystemModel


class FileExplorer(QTreeView):
    def __init__(self):
        super().__init__()
        # 使用 QFileSystemModel 作为数据模型，显示文件系统结构
        self.model = QFileSystemModel()
        self.model.setRootPath("../Export/")
        # 设置模型
        self.setModel(self.model)
        self.setRootIndex(self.model.index("../Export/"))  # 设置根目录

    def set_workspace_path(self, folder_path):
        # 设置工作路径
        self.setRootIndex(self.model.index(folder_path))
