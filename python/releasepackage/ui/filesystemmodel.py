# third party modules
from PySide2 import QtWidgets, QtCore


class FileSystemModel(QtWidgets.QFileSystemModel):
    def __init__(self, *args, **kwargs):
        super(FileSystemModel, self).__init__(*args, **kwargs)
        self._custom_columns = ["file_type", "destination"]
        self._custom_data = {}

    def columnCount(self, parent_index=QtCore.QModelIndex()):
        count = super(FileSystemModel, self).columnCount(parent_index)
        count += len(self._custom_columns)
        return count

    def data(self, index, role):
        column = index.column()
        count = super(FileSystemModel, self).columnCount()
        if column < count:
            return super(FileSystemModel, self).data(index, role)

        if role == QtCore.Qt.DisplayRole:
            try:
                index_data = self._custom_data[index]
                return index_data[column]
            except KeyError:
                return ""

    def headerData(self, section, orientation=QtCore.Qt.Horizontal, role=QtCore.Qt.DisplayRole):
        count = super(FileSystemModel, self).columnCount()
        if section < count:
            return super(FileSystemModel, self).headerData(section, orientation, role)

        label = self._custom_columns[section - count]
        return label.replace("_", " ").title()

    def setData(self, index, value, role):
        column = index.column()
        count = super(FileSystemModel, self).columnCount()
        if column < count:
            return super(FileSystemModel, self).setData(index, value, role)

        index_data = self._custom_data.setdefault(index, {})
        index_data.setdefault(column, value)
        self.dataChanged.emit(index, index)
