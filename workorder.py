

# pyinstaller --onefile --windowed --name "WorkOrderEditor" --icon="icon.ico" workorder.py

import sys
import os
import configparser
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QRadioButton, QLabel, QComboBox, QPushButton, QInputDialog, QMessageBox,
    QDialog, QLineEdit, QFileDialog
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


# -------------------------
# Settings Dialog
# -------------------------
class SettingsDialog(QDialog):
    def __init__(self, files, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuration File Paths")
        self.setFixedSize(500, 400)
        self.files = files.copy()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        grid = QGridLayout()
        grid.setSpacing(6)

        self.path_inputs = {}

        for i, (name, path) in enumerate(self.files.items()):
            label = QLabel(name)
            line_edit = QLineEdit(path)
            browse_btn = QPushButton("Browse")
            browse_btn.clicked.connect(lambda checked, n=name: self.browse_file(n))

            self.path_inputs[name] = line_edit

            grid.addWidget(label, i, 0)
            grid.addWidget(line_edit, i, 1)
            grid.addWidget(browse_btn, i, 2)

        layout.addLayout(grid)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save Paths")
        cancel_btn = QPushButton("Cancel")

        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def browse_file(self, name):
        filename, _ = QFileDialog.getOpenFileName(
            self, f"Select {name}", "", "INI Files (*.ini);;All Files (*.*)"
        )
        if filename:
            self.path_inputs[name].setText(filename)

    def get_paths(self):
        return {k: v.text() for k, v in self.path_inputs.items()}


# -------------------------
# Main Window
# -------------------------
class ConfigEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        # -------------------------
        # EXE / Script Directory Handling
        # -------------------------
        if getattr(sys, "frozen", False):
            self.script_dir = os.path.dirname(sys.executable)
            self.base_path = sys._MEIPASS
        else:
            self.script_dir = os.path.dirname(os.path.abspath(__file__))
            self.base_path = self.script_dir

        self.setWindowTitle("Work Order Editor")

        icon_path = os.path.join(self.base_path, "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setGeometry(200, 200, 400, 380)

        # -------------------------
        # Files and Defaults
        # -------------------------
        self.settings_file = os.path.join(self.script_dir, "settings.ini")
        self.options_file = os.path.join(self.script_dir, "options.ini")
        self.prefix = " Your prefix"

        self.default_files = {
            "model_1": os.path.join(self.script_dir, "model_1.ini"),
            "model_2": os.path.join(self.script_dir, "model_2.ini"),
            "model_3": os.path.join(self.script_dir, "model_3.ini"),
            "model_4": os.path.join(self.script_dir, "model_4.ini"),
            "model_5": os.path.join(self.script_dir, "model_5.ini"),
        }

        self.files = self.load_settings()

        self.default_options = {
            "model_1": ["OptionA", "OptionB", "OptionC"],
            "model_2": ["OptionD", "OptionE", "OptionF"],
            "model_3": ["OptionG", "OptionH", "OptionI"],
            "model_4": ["OptionJ", "OptionK", "OptionL"],
            "model_5": ["OptionM", "OptionN", "OptionO"],
        }

        self.current_options = []
        self.selected_config = None

        # -------------------------
        # Initialize UI
        # -------------------------
        self.create_menu()
        self.init_ui()
        self.check_single_instance()

    # -------------------------
    # Menu
    # -------------------------
    def create_menu(self):
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("&Settings")
        settings_action = settings_menu.addAction("&Config Paths...")
        settings_action.setShortcut("Ctrl+P")
        settings_action.triggered.connect(self.show_settings)

    # -------------------------
    # Load / Save Settings
    # -------------------------
    def load_settings(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.settings_file):
            config.read(self.settings_file, encoding="utf-8")

        paths = {}
        for name in self.default_files:
            if config.has_option("Paths", name):
                paths[name] = config.get("Paths", name)
            else:
                paths[name] = self.default_files[name]

        return paths

    def save_settings(self, paths):
        config = configparser.ConfigParser()
        config["Paths"] = paths
        with open(self.settings_file, "w", encoding="utf-8") as f:
            config.write(f)
        self.files = paths
        QMessageBox.information(self, "Saved", "Config paths saved successfully!")

    def show_settings(self):
        dialog = SettingsDialog(self.files, self)
        if dialog.exec():
            self.save_settings(dialog.get_paths())

    # -------------------------
    # Single Instance
    # -------------------------
    def check_single_instance(self):
        # Using lock file
        lock_file = os.path.join(self.script_dir, "WorkOrderEditor.lock")
        if os.path.exists(lock_file):
            QMessageBox.information(
                self, "Already Running", "Work Order Editor is already running."
            )
            sys.exit()
        else:
            with open(lock_file, "w") as f:
                f.write(str(os.getpid()))

    # -------------------------
    # UI Layout
    # -------------------------
    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)

        # Config selection
        layout.addWidget(QLabel("Select Configuration:"))
        self.radio_group = QWidget()
        radio_layout = QVBoxLayout(self.radio_group)
        radio_layout.setSpacing(4)
        self.radios = {}

        for name in self.files.keys():
            radio = QRadioButton(name)
            radio.toggled.connect(self.on_radio_changed)
            radio_layout.addWidget(radio)
            self.radios[name] = radio

        layout.addWidget(self.radio_group)

        # WorkOrder selection
        layout.addWidget(QLabel("WorkOrder value:"))
        self.combo = QComboBox()
        self.combo.setStyleSheet("padding:4px; font-size:12px;")
        layout.addWidget(self.combo)

        # Preview
        self.preview_label = QLabel("No file selected")
        self.preview_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self.preview_label)

        # Buttons
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Option")
        self.add_btn.setStyleSheet("""
            QPushButton { background:#0078d4; color:white; padding:4px; border-radius:3px;}
            QPushButton:hover { background:#005a9e;}
        """)
        self.submit_btn = QPushButton("OK")
        self.submit_btn.setDefault(True)
        self.submit_btn.setStyleSheet("""
            QPushButton { background:#28a745; color:white; padding:4px; border-radius:3px;}
            QPushButton:hover { background:#1e7e34;}
        """)
        self.add_btn.clicked.connect(self.add_option)
        self.submit_btn.clicked.connect(self.submit)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.submit_btn)
        layout.addLayout(btn_layout)

        central.setLayout(layout)

    # -------------------------
    # Logic
    # -------------------------
    def on_radio_changed(self):
        self.selected_config = None
        for name, radio in self.radios.items():
            if radio.isChecked():
                self.selected_config = name
                break
        if self.selected_config:
            self.load_options()
            self.update_preview()
        else:
            self.combo.clear()
            self.preview_label.setText("No file selected")

    def load_options(self):
        self.current_options = self.default_options.get(self.selected_config, [])
        config = configparser.ConfigParser()
        if os.path.exists(self.options_file):
            config.read(self.options_file, encoding="utf-8")
            if config.has_section(self.selected_config):
                options = config[self.selected_config].get("WorkOrderOptions", "")
                self.current_options = [o.strip() for o in options.split("|") if o.strip()]
        self.combo.clear()
        self.combo.addItems(self.current_options)

    def add_option(self):
        if not self.selected_config:
            QMessageBox.warning(self, "Error", "Select a configuration first.")
            return
        new_option, ok = QInputDialog.getText(self, "Add Option", "Enter new option:")
        if ok and new_option.strip() and new_option.strip() not in self.current_options:
            self.current_options.append(new_option.strip())
            self.save_options()
            self.combo.clear()
            self.combo.addItems(self.current_options)

    def save_options(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.options_file):
            config.read(self.options_file, encoding="utf-8")
        if self.selected_config not in config:
            config[self.selected_config] = {}
        config[self.selected_config]["WorkOrderOptions"] = "|".join(self.current_options)
        with open(self.options_file, "w", encoding="utf-8") as f:
            config.write(f)

    def update_preview(self):
        file_path = self.files.get(self.selected_config)
        if not file_path or not os.path.exists(file_path):
            self.preview_label.setText("File missing")
            self.preview_label.setStyleSheet("color: red; font-style: italic;")
            return
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.strip().startswith(self.prefix):
                    value = line.strip().split("=", 1)[1]
                    self.preview_label.setText(f"Current: {value}")
                    self.preview_label.setStyleSheet("color: green; font-style: italic;")
                    return
        self.preview_label.setText("SoMoNo not found")
        self.preview_label.setStyleSheet("color: orange; font-style: italic;")

    def submit(self):
        if not self.selected_config:
            QMessageBox.warning(self, "Error", "Select a configuration first.")
            return
        work_order = self.combo.currentText()
        if not work_order:
            QMessageBox.warning(self, "Error", "Select a WorkOrder value.")
            return
        config_file = self.files.get(self.selected_config)
        if not config_file or not os.path.exists(config_file):
            QMessageBox.warning(self, "Error", "Config file missing.")
            return
        with open(config_file, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if line.strip().startswith(self.prefix):
                lines[i] = f"{self.prefix}{work_order}\n"
                break
        with open(config_file, "w", encoding="utf-8") as f:
            f.writelines(lines)
        QMessageBox.information(self, "Success", "WorkOrder updated successfully.")
        self.close()

    def closeEvent(self, event):
        lock_file = os.path.join(self.script_dir, "WorkOrderEditor.lock")
        if os.path.exists(lock_file):
            os.remove(lock_file)
        event.accept()


# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConfigEditor()
    window.show()
    sys.exit(app.exec())