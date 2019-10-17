# stdlib modules
import os

# tool modules
from launchcmd import gitutils
from launchcmd.ui.filesystemtreewidget import FileSystemTreeWidget
from launchcmd.ui.errordialog import ErrorDialog
from launchcmd import packageutils

# third party modules
from PySide2 import QtWidgets, QtCore


class ReleasePackageDialog(QtWidgets.QDialog):
    """GUI to release a repository as a launchcmd package."""

    def __init__(self, module_file, *args, **kwargs):
        """Initializes the object.

        :param repository_directory: Absolute directory of the repository.
        :type repository_directory: str
        """
        super(ReleasePackageDialog, self).__init__(*args, **kwargs)

        # ensure module file exists
        if not os.path.exists(module_file):
            raise IOError("module file does not exist: {}".format(module_file))

        # ensure modulefile is in root of git repository
        repo_dir = os.path.dirname(module_file)
        gitutils.validate_directory_is_repository(repo_dir)

        self._module_file = module_file
        self._build_ui()
        self._connect_signals()
        self._initialize(repo_dir)

    # =========================================================================
    # private
    # =========================================================================
    def _build_ui(self):
        """Builds the user interface."""
        # version
        self._sb_major = QtWidgets.QSpinBox()
        self._sb_minor = QtWidgets.QSpinBox()
        self._sb_patch = QtWidgets.QSpinBox()

        self._btn_major_up = QtWidgets.QPushButton("+")
        self._btn_minor_up = QtWidgets.QPushButton("+")
        self._btn_patch_up = QtWidgets.QPushButton("+")

        spin_box_layout = QtWidgets.QHBoxLayout()
        spin_box_layout.addWidget(self._sb_major)
        spin_box_layout.addWidget(self._sb_minor)
        spin_box_layout.addWidget(self._sb_patch)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self._btn_major_up)
        button_layout.addWidget(self._btn_minor_up)
        button_layout.addWidget(self._btn_patch_up)

        group_box_version = QtWidgets.QGroupBox("Version:")
        group_box_version_layout = QtWidgets.QVBoxLayout()
        group_box_version_layout.addLayout(spin_box_layout)
        group_box_version_layout.addLayout(button_layout)
        group_box_version.setLayout(group_box_version_layout)

        # comment
        self._te_comment = QtWidgets.QTextEdit()

        group_box_comment = QtWidgets.QGroupBox("Comment:")
        group_box_comment_layout = QtWidgets.QVBoxLayout()
        group_box_comment_layout.addWidget(self._te_comment)
        group_box_comment.setLayout(group_box_comment_layout)

        # tree view
        self._tree_widget = FileSystemTreeWidget()

        group_box_tree = QtWidgets.QGroupBox("Files:")
        group_box_tree_layout = QtWidgets.QVBoxLayout()
        group_box_tree_layout.addWidget(self._tree_widget)
        group_box_tree.setLayout(group_box_tree_layout)

        # btn release
        self._btn_release = QtWidgets.QPushButton("Release")

        # main layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(group_box_version)
        layout.addWidget(group_box_comment)
        layout.addWidget(group_box_tree)
        layout.setStretch(2, 1)
        layout.addWidget(self._btn_release)
        self.setLayout(layout)

        # window settings
        self.setWindowTitle("ReleasePackge")
        self.setWindowFlags(QtCore.Qt.Window |
                            QtCore.Qt.WindowMinimizeButtonHint |
                            QtCore.Qt.WindowMaximizeButtonHint |
                            QtCore.Qt.WindowCloseButtonHint)
        self.resize(480, 720)

    def _initialize(self, repo_dir):
        """Initializes data to display.

        :param repo_dir: Absolute directory of the repository to release.
        :type repo_dir: str
        """
        self._tree_widget.set_root_directory(repo_dir)

    def _connect_signals(self):
        """Connects the user interface signals with slots."""
        self._btn_major_up.released.connect(self._btn_major_up_released)
        self._btn_minor_up.released.connect(self._btn_minor_up_released)
        self._btn_patch_up.released.connect(self._btn_patch_up_released)
        self._tree_widget.itemChanged.connect(self._item_changed)
        self._btn_release.released.connect(self._btn_release_released)

    def _btn_major_up_released(self):
        """Increases the major version and resets the minor and patch version."""
        self._sb_major.setValue(self._sb_major.value() + 1)
        self._sb_minor.setValue(0)
        self._sb_patch.setValue(0)

    def _btn_minor_up_released(self):
        """Increases the minor version and resets the patch version."""
        self._sb_minor.setValue(self._sb_minor.value() + 1)
        self._sb_patch.setValue(0)

    def _btn_patch_up_released(self):
        """Increases the patch version."""
        self._sb_patch.setValue(self._sb_patch.value() + 1)

    def _item_changed(self, item, column):
        """Propagates the checkstate of changed item to all its children.

        :param item: Item where data was changed.
        :type item: QtWidgets.QTreeWidgetItem

        :param column: Column the data was changed in.
        :type column: int
        """
        state = item.checkState(column)

        for i in range(item.childCount()):
            child_item = item.child(i)
            child_item.setCheckState(column, state)

    def _btn_release_released(self):
        repo_dir = self._tree_widget.root_directory
        package = os.path.splitext(os.path.basename(self._module_file))[0]
        version = self.version
        comment = self.comment
        files = self.checked_files

        try:
            packageutils.release_package(repo_dir, package, version, comment, files)
            msg = "Successfully release package (name={}, version={})."
            QtWidgets.QMessageBox.information(self, self.windowTitle(), msg.format(package, version))
            self.accept()
        except Exception as e:
            msg = "Could not release package (name={}, version={})."
            ErrorDialog(self.windowTitle(), msg.format(package, version), str(e)).exec_()

    # =========================================================================
    # public
    # =========================================================================
    @property
    def major_version(self):
        """Returns the major version.

        :rtype: int
        """
        return self._sb_major.value()

    @property
    def minor_version(self):
        """Returns the minor version.

        :rtype: int
        """
        return self._sb_minor.value()

    @property
    def patch_version(self):
        """Returns the patch version.

        :rtype: int
        """
        return self._sb_patch.value()

    @property
    def version(self):
        """Returns the full version.

        :rtype: str
        """
        parts = [self.major_version, self.minor_version, self.patch_version]
        return ".".join(map(str, parts))

    @property
    def comment(self):
        """Returns the comment.

        :rtype: str
        """
        return self._te_comment.toPlainText()

    @property
    def checked_files(self):
        """Returns the checked files from the user interface.

        :rtype: list[str]
        """
        root_item = self._tree_widget.invisibleRootItem()
        items = self._tree_widget.get_checked_items(root_item)
        paths = map(self._tree_widget.get_path_from_item, items)
        files = list(filter(os.path.isfile, paths))
        return files
