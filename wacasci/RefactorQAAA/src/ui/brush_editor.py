# src/ui/brush_editor.py
from __future__ import annotations

from typing import Callable, Dict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
)


class BrushEditorDialog(QDialog):
    """
    Edits named brush patterns. The window doesn't own brushes; it edits a dict via callbacks.
    """
    def __init__(
        self,
        parent=None,
        get_brushes: Callable[[], Dict[str, str]] = None,
        set_brush: Callable[[str, str], None] = None,
    ):
        super().__init__(parent)
        self.setWindowTitle("Edit Brushes")
        self.setWindowFlags(Qt.Window)

        self._get_brushes = get_brushes
        self._set_brush = set_brush

        layout = QVBoxLayout()
        self._edits: Dict[str, QLineEdit] = {}

        brushes = dict(self._get_brushes()) if self._get_brushes else {}
        for name in brushes.keys():
            row = QHBoxLayout()
            lbl = QLabel(name + ":")
            edit = QLineEdit(brushes[name])
            btn = QPushButton("Save")

            def make_save(nm: str, ed: QLineEdit):
                def save():
                    val = ed.text()
                    if self._set_brush:
                        self._set_brush(nm, val)
                return save

            btn.clicked.connect(make_save(name, edit))

            row.addWidget(lbl)
            row.addWidget(edit)
            row.addWidget(btn)

            self._edits[name] = edit
            layout.addLayout(row)

        self.setLayout(layout)
        self.resize(760, 320)

    def show_or_raise(self):
        if self.isVisible():
            self.raise_()
            self.activateWindow()
        else:
            self.show()
