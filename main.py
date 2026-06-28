#!/usr/bin/env python3
# ============================================================
# NEXUS EXECUTOR — ANDROID GUI EDITION
# AUTHOR: PROFESOR_FATIH + NEXUS 1.0
# ============================================================

import os
import sys
import json
import requests
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QTextEdit, QLineEdit, QLabel, QFileDialog,
    QMessageBox, QTabWidget, QGroupBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor

# ============================================================
# KONFIGURASI
# ============================================================

VERSION = "1.0.0"
AUTHOR = "PROFESOR_FATIH + NEXUS 1.0"
SCRIPT_DIR = os.path.expanduser("~/nexus_executor/scripts")
LOG_DIR = os.path.expanduser("~/nexus_executor/logs")
os.makedirs(SCRIPT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# ============================================================
# FUNGSI UTILITY
# ============================================================

def get_timestamp():
    return datetime.now().strftime("%H:%M:%S")

def log_message(msg):
    with open(os.path.join(LOG_DIR, "execution.log"), "a") as f:
        f.write(f"[{get_timestamp()}] {msg}\n")

# ============================================================
# THREAD EKSEKUSI SCRIPT (AGAR GUI TETAP RESPONSIF)
# ============================================================

class ExecuteThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, script_content):
        super().__init__()
        self.script_content = script_content

    def run(self):
        try:
            # Simulasi eksekusi script
            lines = self.script_content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('print('):
                    content = line[6:-1].strip('"\'')
                    self.log_signal.emit(f"📤 {content}")
                elif line.startswith('--'):
                    self.log_signal.emit(f"💬 {line[2:]}")
                elif line.startswith('loadstring'):
                    self.log_signal.emit("📥 loadstring detected, simulating...")
            self.log_signal.emit("✅ Script executed successfully!")
        except Exception as e:
            self.log_signal.emit(f"❌ Error: {e}")
        self.finished_signal.emit()

# ============================================================
# MAIN WINDOW
# ============================================================

class NexusUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"NEXUS EXECUTOR — ANDROID v{VERSION}")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow { background-color: #1a1a2e; }
            QLabel { color: #00ff88; font-weight: bold; }
            QPushButton {
                background-color: #16213e;
                color: #00ff88;
                border: 1px solid #00ff88;
                border-radius: 8px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ff88;
                color: #1a1a2e;
            }
            QListWidget {
                background-color: #0f0f1a;
                color: #aabbcc;
                border: 1px solid #00ff88;
                border-radius: 8px;
                padding: 5px;
            }
            QTextEdit, QLineEdit {
                background-color: #0f0f1a;
                color: #aabbcc;
                border: 1px solid #00ff88;
                border-radius: 8px;
                padding: 5px;
            }
            QTabWidget::pane {
                border: 1px solid #00ff88;
                border-radius: 8px;
                background-color: #1a1a2e;
            }
            QTabBar::tab {
                background-color: #16213e;
                color: #aabbcc;
                padding: 8px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: #00ff88;
                color: #1a1a2e;
            }
        """)
        
        self.init_ui()
        self.load_script_list()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # ============================================================
        # HEADER
        # ============================================================
        header = QLabel("☠️ NEXUS EXECUTOR — ANDROID GUI")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 18, QFont.Bold))
        main_layout.addWidget(header)

        # ============================================================
        # TAB WIDGET
        # ============================================================
        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        # --- TAB 1: SCRIPT MANAGER ---
        script_tab = QWidget()
        script_layout = QVBoxLayout(script_tab)

        # List Scripts
        self.script_list = QListWidget()
        self.script_list.itemClicked.connect(self.load_selected_script)
        script_layout.addWidget(QLabel("📚 Scripts:"))
        script_layout.addWidget(self.script_list)

        # Buttons for Scripts
        btn_layout = QHBoxLayout()
        self.load_btn = QPushButton("📥 Load Script")
        self.load_btn.clicked.connect(self.load_selected_script)
        btn_layout.addWidget(self.load_btn)
        
        self.download_btn = QPushButton("⬇️ Download Script")
        self.download_btn.clicked.connect(self.download_script)
        btn_layout.addWidget(self.download_btn)

        self.delete_btn = QPushButton("🗑️ Delete Script")
        self.delete_btn.clicked.connect(self.delete_script)
        btn_layout.addWidget(self.delete_btn)

        script_layout.addLayout(btn_layout)

        # Script Content
        script_layout.addWidget(QLabel("📜 Script Content:"))
        self.script_content = QTextEdit()
        script_layout.addWidget(self.script_content)

        # Execute Button
        self.execute_btn = QPushButton("▶️ EXECUTE SCRIPT")
        self.execute_btn.clicked.connect(self.execute_script)
        script_layout.addWidget(self.execute_btn)

        tabs.addTab(script_tab, "📜 Scripts")

        # --- TAB 2: OUTPUT LOG ---
        log_tab = QWidget()
        log_layout = QVBoxLayout(log_tab)
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        log_layout.addWidget(QLabel("📤 Output Log:"))
        log_layout.addWidget(self.log_output)
        tabs.addTab(log_tab, "📤 Log")

        # --- TAB 3: CREATE SCRIPT ---
        create_tab = QWidget()
        create_layout = QVBoxLayout(create_tab)
        create_layout.addWidget(QLabel("📝 Create New Script:"))
        
        self.new_script_name = QLineEdit()
        self.new_script_name.setPlaceholderText("script_name.lua")
        create_layout.addWidget(self.new_script_name)
        
        self.new_script_content = QTextEdit()
        self.new_script_content.setPlaceholderText("-- Write your script here...")
        create_layout.addWidget(self.new_script_content)
        
        self.save_btn = QPushButton("💾 Save Script")
        self.save_btn.clicked.connect(self.save_script)
        create_layout.addWidget(self.save_btn)
        
        tabs.addTab(create_tab, "📝 Create")

        # ============================================================
        # STATUS BAR
        # ============================================================
        self.statusBar().showMessage("Ready")

    # ============================================================
    # FUNGSI SCRIPT MANAGER
    # ============================================================

    def load_script_list(self):
        """Load all .lua scripts from the scripts directory"""
        self.script_list.clear()
        try:
            scripts = [f for f in os.listdir(SCRIPT_DIR) if f.endswith('.lua')]
            if scripts:
                self.script_list.addItems(scripts)
            else:
                self.script_list.addItem("📂 No scripts found")
        except Exception as e:
            self.log(f"Error loading scripts: {e}")

    def load_selected_script(self):
        """Load selected script content into the text editor"""
        selected = self.script_list.currentItem()
        if not selected or selected.text() == "📂 No scripts found":
            return
        
        filename = selected.text()
        path = os.path.join(SCRIPT_DIR, filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.script_content.setText(content)
            self.log(f"✅ Loaded: {filename}")
        except Exception as e:
            self.log(f"❌ Error loading script: {e}")

    def download_script(self):
        """Download a script from URL"""
        url, ok = QInputDialog.getText(self, "Download Script", "Enter script URL:")
        if not ok or not url:
            return
        
        name, ok = QInputDialog.getText(self, "Download Script", "Save as (with .lua):")
        if not ok or not name:
            return
        if not name.endswith('.lua'):
            name += '.lua'
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                path = os.path.join(SCRIPT_DIR, name)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                self.log(f"✅ Downloaded: {name}")
                self.load_script_list()
            else:
                self.log(f"❌ Failed: HTTP {response.status_code}")
        except Exception as e:
            self.log(f"❌ Error: {e}")

    def delete_script(self):
        """Delete selected script"""
        selected = self.script_list.currentItem()
        if not selected or selected.text() == "📂 No scripts found":
            return
        
        filename = selected.text()
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            f"Delete '{filename}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                os.remove(os.path.join(SCRIPT_DIR, filename))
                self.log(f"🗑️ Deleted: {filename}")
                self.load_script_list()
                self.script_content.clear()
            except Exception as e:
                self.log(f"❌ Error deleting: {e}")

    def save_script(self):
        """Save new script from the create tab"""
        name = self.new_script_name.text().strip()
        content = self.new_script_content.toPlainText().strip()
        if not name:
            self.log("❌ Please enter a script name.")
            return
        if not name.endswith('.lua'):
            name += '.lua'
        if not content:
            self.log("❌ Please enter script content.")
            return
        
        path = os.path.join(SCRIPT_DIR, name)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.log(f"✅ Saved: {name}")
            self.new_script_name.clear()
            self.new_script_content.clear()
            self.load_script_list()
        except Exception as e:
            self.log(f"❌ Error saving: {e}")

    def execute_script(self):
        """Execute the current script in a separate thread"""
        content = self.script_content.toPlainText().strip()
        if not content:
            self.log("⚠️ No script to execute!")
            return
        
        self.log("▶️ Executing script...")
        self.execute_btn.setEnabled(False)
        self.thread = ExecuteThread(content)
        self.thread.log_signal.connect(self.log)
        self.thread.finished_signal.connect(lambda: self.execute_btn.setEnabled(True))
        self.thread.start()

    def log(self, message):
        """Add message to log and status bar"""
        timestamp = get_timestamp()
        log_msg = f"[{timestamp}] {message}"
        self.log_output.append(log_msg)
        self.statusBar().showMessage(message, 3000)
        log_message(message)

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set dark palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(26, 26, 46))
    palette.setColor(QPalette.WindowText, QColor(0, 255, 136))
    palette.setColor(QPalette.Base, QColor(15, 15, 26))
    palette.setColor(QPalette.AlternateBase, QColor(22, 33, 62))
    palette.setColor(QPalette.ToolTipBase, QColor(0, 255, 136))
    palette.setColor(QPalette.ToolTipText, QColor(26, 26, 46))
    palette.setColor(QPalette.Text, QColor(170, 187, 204))
    palette.setColor(QPalette.Button, QColor(22, 33, 62))
    palette.setColor(QPalette.ButtonText, QColor(0, 255, 136))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Highlight, QColor(0, 255, 136))
    palette.setColor(QPalette.HighlightedText, QColor(26, 26, 46))
    app.setPalette(palette)
    
    window = NexusUI()
    window.show()
    sys.exit(app.exec_())
