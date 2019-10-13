# stdlib modules
import os

# tool modules
from releasepackage.ui.filesystemmodel import FileSystemModel

# third party modules
from PySide2 import QtWidgets


class ReleasePackageDialog(QtWidgets.QDialog):
    def __init__(self, manifest_file, *args, **kwargs):
        super(ReleasePackageDialog, self).__init__(*args, **kwargs)

        self._manifest_path = manifest_file
        self._package_root = os.path.dirname(self._manifest_path)
        self._package_name = os.path.basename(self._manifest_path)
        self._model = FileSystemModel()

        self._build_ui()
        self._initialize()

    def _build_ui(self):
        """Builds the user inteface."""
        # tree view
        self._tree_view = QtWidgets.QTreeView()
        self._tree_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self._tree_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self._tree_view.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        # btn continue
        self._btn_continue = QtWidgets.QPushButton("Continue")

        # main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self._tree_view)
        main_layout.addWidget(self._btn_continue)
        self.setLayout(main_layout)

        # window settings
        self.setWindowTitle("ReleasePackage GUI")
        self.resize(720, 480)

    def _initialize(self):
        self._model.setRootPath(self._package_root)
        self._tree_view.setModel(self._model)
        self._tree_view.setRootIndex(self._model.index(self._package_root))
