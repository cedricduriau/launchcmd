# stdlib modules
import os

# third party modules
from PySide2 import QtWidgets, QtCore


class FileSystemTreeWidget(QtWidgets.QTreeWidget):
    """Tree widget displaying file system entries."""

    def __init__(self, *args, **kwargs):
        """Initializes the object."""
        super(FileSystemTreeWidget, self).__init__(*args, **kwargs)

        self.setHeaderLabels(["Name"])
        self._root_dir = ""
        self._items_by_path = {}

    # =========================================================================
    # private
    # =========================================================================
    def _build_item(self, path, parent=None, column=0):
        """Buids a tree item.

        :param path: Path of the file/directory to display.
        :type path: str

        :param parent: Parent item to attach item to.
        :type parent: QtWidgets.QTreeWidgetItem

        :param column: Column index holding the data to display.
        :type column: int

        :rtype: QtWidgets.QTreeWidgetItem
        """
        # build item
        item = QtWidgets.QTreeWidgetItem(parent)
        item.setCheckState(column, QtCore.Qt.Unchecked)
        item.setText(column, os.path.basename(path))
        item.setData(0, QtCore.Qt.UserRole, path)

        # set icon
        if os.path.isfile(path):
            filetype = QtWidgets.QFileIconProvider.File
        else:
            filetype = QtWidgets.QFileIconProvider.Folder

        icon = QtWidgets.QFileIconProvider().icon(filetype)
        item.setIcon(column, icon)

        # cache item
        self._items_by_path[path] = item

        return item

    # =========================================================================
    # public
    # =========================================================================
    @property
    def root_directory(self):
        """Returns the root directory currently set.

        :rtype: str
        """
        return self._root_dir

    def set_root_directory(self, root_directory):
        """Sets the root directory and displays all underlying files/dirs.

        :param root_directory: Root directory to display content from.
        :type root_directory: str
        """
        # clear cache
        self._items_by_path.clear()
        self._root_dir = root_directory

        prev_parent_item = self.invisibleRootItem()
        for root_dir, dirs, files in os.walk(root_directory):
            if root_dir == root_directory:
                parent_item = prev_parent_item
            else:
                parent_item = self._items_by_path[root_dir]

            for d in sorted(dirs):
                self._build_item(os.path.join(root_dir, d), parent=parent_item)

            for f in sorted(files):
                self._build_item(os.path.join(root_dir, f), parent=parent_item)

    def find_item(self, path):
        """Finds a tree item by path.

        :param path: Absolute path of the item to find.
        :type path: str

        :rtype: QtWidgets.QTreeWidgetItem or None
        """
        return self._items_by_path.get(path)

    def get_checked_items(self, item):
        """Returns the checked items starting at a specific item.

        :param item: Item to start searching recursively for checked items.
        :type item: QtWidgets.QTreeWidgetItem

        :rtype: list[QtWidgets.QTreeWidgetItem]
        """
        items = []

        if item.checkState(0) == QtCore.Qt.Checked:
            items.append(item)

        for i in range(item.childCount()):
            child_item = item.child(i)
            items.extend(self.get_checked_items(child_item))

        return items

    def get_path_from_item(self, item):
        """Returns the absolute path from an item.

        :param item: Item to get path from.
        :type item: QtWidgets.QTreeWidgetItem

        :rtype: str or None
        """
        return item.data(0, QtCore.Qt.UserRole)
