# third party modules
from PySide2 import QtWidgets


class ErrorDialog(QtWidgets.QDialog):
    """Dialog displaying an error with detailed information."""

    def __init__(self, title, brief, details, *args, **kwargs):
        """Initializes the object.

        :param title: Window title.
        :type title: str

        :param brief: Short description of the error message.
        :type brief: str

        :param details: Detailed description of the error message.
        :type details: str
        """
        super(ErrorDialog, self).__init__(*args, **kwargs)

        # brief
        lbl_brief = QtWidgets.QLabel(brief)
        lbl_brief.setStyleSheet("QLabel {color : red}")

        # details
        te_details = QtWidgets.QPlainTextEdit()
        te_details.setPlainText(details)

        # button
        btn_close = QtWidgets.QPushButton("Close")
        btn_close.released.connect(self.accept)

        # main layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(lbl_brief)
        layout.addWidget(te_details)
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch(0)
        button_layout.addWidget(btn_close)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # window settings
        self.setWindowTitle(title)
