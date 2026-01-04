# src/ui/control_panel.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton,
    QCheckBox
)


@dataclass
class ControlState:
    char_width: int
    char_height: int
    show_cursor: bool
    bg_transparent: bool
    vector_commit_on_release: bool


class ControlPanelDialog(QDialog):
    def __init__(
        self,
        parent=None,
        get_state: Callable[[], ControlState] = None,
        apply_state: Callable[[ControlState], None] = None,
    ):
        super().__init__(parent)
        self.setWindowTitle("Control Panel")
        self.setWindowFlags(Qt.Window)

        self._get_state = get_state
        self._apply_state = apply_state

        s = self._get_state() if self._get_state else ControlState(8, 24, False, True, True)

        layout = QVBoxLayout()

        # char width / height
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Cell width:"))
        self.sp_w = QSpinBox()
        self.sp_w.setRange(2, 80)
        self.sp_w.setValue(s.char_width)
        row1.addWidget(self.sp_w)

        row1.addWidget(QLabel("Cell height:"))
        self.sp_h = QSpinBox()
        self.sp_h.setRange(4, 120)
        self.sp_h.setValue(s.char_height)
        row1.addWidget(self.sp_h)

        layout.addLayout(row1)

        # toggles
        self.cb_cursor = QCheckBox("Show cursor")
        self.cb_cursor.setChecked(s.show_cursor)
        layout.addWidget(self.cb_cursor)

        self.cb_bg = QCheckBox("Transparent background")
        self.cb_bg.setChecked(s.bg_transparent)
        layout.addWidget(self.cb_bg)

        self.cb_vec = QCheckBox("Vector: commit on mouse release")
        self.cb_vec.setChecked(s.vector_commit_on_release)
        layout.addWidget(self.cb_vec)

        # buttons
        row_btn = QHBoxLayout()
        btn_apply = QPushButton("Apply")
        btn_close = QPushButton("Close")
        row_btn.addWidget(btn_apply)
        row_btn.addWidget(btn_close)
        layout.addLayout(row_btn)

        def do_apply():
            st = ControlState(
                char_width=int(self.sp_w.value()),
                char_height=int(self.sp_h.value()),
                show_cursor=bool(self.cb_cursor.isChecked()),
                bg_transparent=bool(self.cb_bg.isChecked()),
                vector_commit_on_release=bool(self.cb_vec.isChecked()),
            )
            if self._apply_state:
                self._apply_state(st)

        btn_apply.clicked.connect(do_apply)
        btn_close.clicked.connect(self.close)

        self.setLayout(layout)
        self.resize(520, 240)

    def show_or_raise(self):
        if self.isVisible():
            self.raise_()
            self.activateWindow()
        else:
            self.show()
