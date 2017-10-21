import json

from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QHeaderView


class MainWindow(QMainWindow):
    def __init__(self):
        # noinspection PyArgumentList
        QMainWindow.__init__(self)
        uic.loadUi('qt/CreateView.ui', self)
        self.settings = QSettings(QSettings.IniFormat, QSettings.UserScope, "KestinGoforth", "ClooneySheetGen")

        self.fields_fp_button.clicked.connect(self.fields_filepath_clicked)
        self.config_fp_button.clicked.connect(self.config_filepath_clicked)
        self.sheets_fp_button.clicked.connect(self.sheets_filepath_clicked)

        self.event_name.setText(self.settings.value("event_name", ""))
        self.num_matches.setValue(int(self.settings.value("num_matches", 0)))
        self.add_spacer_page.setChecked(self.settings.value("spacer_page", "true") == "true")
        self.config_filepath.setText(self.settings.value("config_filepath", ""))
        self.fields_filepath.setText(self.settings.value("fields_filepath", ""))
        self.sheets_filepath.setText(self.settings.value("sheets_filepath", ""))

        self.fields = json.load(open("resources/steamworks.json"))

        self.event_name.textChanged.connect(self.edit_event_name)
        self.num_matches.valueChanged.connect(self.edit_num_matches)
        self.add_spacer_page.toggled.connect(self.toggle_spacer_sheet)

        self.setup_fields_list()

        self.show()

    def setup_fields_list(self):
        self.field_view.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        model = QStandardItemModel()
        model.setColumnCount(2)
        for i in range(len(self.fields)):
            field = self.fields[i]
            if field["type"] == "Barcode":
                continue
            if "x_pos" in field.keys():
                del field["x_pos"]
            if "y_pos" in field.keys():
                del field["y_pos"]
            if "height" in field.keys():
                del field["height"]
            field_item = QStandardItem(field["type"])
            field_item.setFlags(field_item.flags() & Qt.ItemIsEditable)
            model.appendRow(field_item)
            self.add_fields(field_item, field)
        self.field_view.setModel(model)

    def add_fields(self, parent, elements):
        for text, children in list(elements.items()):
            item = QStandardItem(text)
            item.setFlags(item.flags() & Qt.ItemIsEditable)
            if isinstance(children, dict):
                parent.appendRow(item)
                self.add_fields(item, children)
            else:
                if isinstance(children, list):
                    children = ", ".join(children)
                value_item = QStandardItem(str(children))
                if text == "type":
                    value_item.setFlags(value_item.flags() & Qt.ItemIsEditable)
                parent.appendRow([item, value_item])

    def toggle_spacer_sheet(self):
        self.settings.setValue("spacer_page", self.add_spacer_page.isChecked())

    def edit_num_matches(self):
        self.settings.setValue("num_matches", self.num_matches.value())

    def edit_event_name(self):
        self.settings.setValue("event_name", self.event_name.text())

    def fields_filepath_clicked(self):
        fp = QFileDialog.getSaveFileName(self, "Save Field Settings File", "fields.json", filter="*.json")[0]
        self.settings.setValue("fields_filepath", fp)
        self.fields_filepath.setText(fp)

    def config_filepath_clicked(self):
        fp = QFileDialog.getSaveFileName(self, "Save Sheet Config File", "config.json", filter="*.json")[0]
        self.settings.setValue("config_filepath", fp)
        self.config_filepath.setText(fp)

    def sheets_filepath_clicked(self):
        fp = QFileDialog.getSaveFileName(self, "Save Sheets", "sheets.pdf", filter="*.pdf")[0]
        self.settings.setValue("sheets_filepath", fp)
        self.sheets_filepath.setText(fp)
