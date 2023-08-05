# -*- coding: utf-8 -*-
import numpy as np
from PySide6 import QtCore, QtGui, QtWidgets

from ..ui import resource_rc
from ..ui.vrtt_widget import Ui_VRTT_Widget


class VRTTWidget(Ui_VRTT_Widget, QtWidgets.QWidget):
    def __init__(
        self,
        lower=0,
        upper=0,
        text="",
        conversion=None,
        mode="text",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        self.text.setText(text)

        self.lower.setMaximum(np.inf)
        self.lower.setMinimum(-np.inf)
        self.lower.setValue(lower)

        self.upper.setMaximum(np.inf)
        self.upper.setMinimum(-np.inf)
        self.upper.setValue(upper)

        self.conversion = conversion

        self.mode_switch.currentIndexChanged.connect(self.mode.setCurrentIndex)

        if mode == "text":
            self.mode_switch.setCurrentIndex(0)
        else:
            self.mode_switch.setCurrentIndex(1)

        self.conversion_btn.clicked.connect(self.edit_conversion)

    def edit_conversion(self):
        dlg = ConversionEditor(
            f"Raw=[{self.lower.value()}, {self.upper.value()}) referenced",
            self.conversion,
            parent=self,
        )
        dlg.exec_()
        if dlg.pressed_button == "apply":
            self.conversion = dlg.conversion()

    def reference(self):
        if self.mode.currentIndex() == 0:
            return self.text.text().strip().encode("utf-8")
        else:
            return self.conversion


from ..dialogs.conversion_editor import ConversionEditor
