# tool modules
from launchcmd import packageutils

# third party modules
from PySide2 import QtWidgets


class PackageNameFormDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(PackageNameFormDialog, self).__init__(*args, **kwargs)

        self._package_name = ""
        self._build_ui()
        self._connect_signals()

    def _build_ui(self):
        self._lbl_package_name = QtWidgets.QLabel("Package Name:")
        self._le_package_name = QtWidgets.QLineEdit()
        self._btn_ok = QtWidgets.QPushButton("&OK")
        self._btn_cancel = QtWidgets.QPushButton("&Cancel")

        # form layout
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(QtWidgets.QLabel("Package name:"), self._le_package_name)

        # button layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self._btn_ok)
        button_layout.addWidget(self._btn_cancel)

        # main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def _connect_signals(self):
        self._le_package_name.textChanged.connect(self._set_package_name)
        self._btn_ok.clicked.connect(self.accept)
        self._btn_cancel.clicked.connect(self.reject)

    def _set_package_name(self, package_name):
        self._package_name = package_name

    @property
    def package_name(self):
        return self._package_name

    def accept(self):
        package_name = self.package_name

        # validate package name
        try:
            packageutils.validate_package_name(package_name)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "ERROR", str(e))
            return

        # close window
        super(PackageNameFormDialog, self).accept()
