from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QFont

import requests
from api import get_auth_headers

BASE_URL = "http://127.0.0.1:8001/api/equipment/history/"

class HistoryLoadWorker(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def run(self):
        try:
            response = requests.get(
                BASE_URL,
                headers=get_auth_headers(),
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            self.finished.emit(data)
        except Exception as e:
            self.error.emit(str(e))


class HistoryDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Upload History")
        self.resize(1100, 650)

        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.setStyleSheet("""
            QDialog {
                background-color: #ecf0f1;
            }
            
            QLabel#title_label {
                color: #2c3e50;
                font-size: 18px;
                font-weight: bold;
                padding: 15px;
            }
            
            QTableWidget {
                background-color: white;
                border: 1px solid #d5dbdb;
                border-radius: 8px;
                gridline-color: #ecf0f1;
                font-size: 12px;
            }
            
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #ecf0f1;
            }
            
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 12px;
            }
            
            QPushButton#btn_close {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 25px;
                font-size: 12px;
                font-weight: 600;
            }
            
            QPushButton#btn_close:hover {
                background-color: #7f8c8d;
            }
            
            QPushButton#btn_refresh {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 25px;
                font-size: 12px;
                font-weight: 600;
            }
            
            QPushButton#btn_refresh:hover {
                background-color: #2980b9;
            }
            
            QLabel#loading_label {
                color: #7f8c8d;
                font-size: 13px;
                font-style: italic;
            }
        """)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title_label = QtWidgets.QLabel("Upload History")
        title_label.setObjectName("title_label")
        layout.addWidget(title_label)

        self.loading_label = QtWidgets.QLabel("Loading history...")
        self.loading_label.setObjectName("loading_label")
        self.loading_label.setAlignment(QtCore.Qt.AlignCenter)
        self.loading_label.hide()
        layout.addWidget(self.loading_label)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Uploaded At",
            "Total Equipment",
            "Avg Flowrate",
            "Avg Pressure",
            "Avg Temperature"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(45)
        self.table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)
        
        layout.addWidget(self.table)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(10)
        
        info_label = QtWidgets.QLabel("Showing last 5 uploads")
        info_label.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        button_layout.addWidget(info_label)
        
        button_layout.addStretch()

        self.btn_refresh = QtWidgets.QPushButton("Refresh")
        self.btn_refresh.setObjectName("btn_refresh")
        self.btn_refresh.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_refresh.clicked.connect(self.load_data)
        button_layout.addWidget(self.btn_refresh)

        btn_close = QtWidgets.QPushButton("Close")
        btn_close.setObjectName("btn_close")
        btn_close.setCursor(QtCore.Qt.PointingHandCursor)
        btn_close.clicked.connect(self.accept)
        button_layout.addWidget(btn_close)

        layout.addLayout(button_layout)

        self.worker = None
        
        self.load_data()

    def load_data(self):
        self.loading_label.show()
        self.table.setRowCount(0)
        self.btn_refresh.setEnabled(False)
        self.btn_refresh.setText("Loading...")
        
        self.worker = HistoryLoadWorker()
        self.worker.finished.connect(self.on_data_loaded)
        self.worker.error.connect(self.on_load_error)
        self.worker.start()

    def on_data_loaded(self, data):
        self.loading_label.hide()
        self.btn_refresh.setEnabled(True)
        self.btn_refresh.setText("Refresh")
        
        if not data:
            self.table.setRowCount(1)
            no_data_item = QtWidgets.QTableWidgetItem("No upload history available")
            no_data_item.setTextAlignment(QtCore.Qt.AlignCenter)
            font = QFont()
            font.setItalic(True)
            no_data_item.setFont(font)
            self.table.setItem(0, 0, no_data_item)
            self.table.setSpan(0, 0, 1, 5)
            return

        self.table.setRowCount(len(data))
        
        for row, item in enumerate(data):
            uploaded_at = QtWidgets.QTableWidgetItem(str(item["uploaded_at"]))
            total = QtWidgets.QTableWidgetItem(str(item["total_equipment"]))
            flowrate = QtWidgets.QTableWidgetItem(f"{item['average_flowrate']:.2f}")
            pressure = QtWidgets.QTableWidgetItem(f"{item['average_pressure']:.2f}")
            temperature = QtWidgets.QTableWidgetItem(f"{item['average_temperature']:.2f}")
            
            for col_item in [total, flowrate, pressure, temperature]:
                col_item.setTextAlignment(QtCore.Qt.AlignCenter)
            
            self.table.setItem(row, 0, uploaded_at)
            self.table.setItem(row, 1, total)
            self.table.setItem(row, 2, flowrate)
            self.table.setItem(row, 3, pressure)
            self.table.setItem(row, 4, temperature)

    def on_load_error(self, error_msg):
        self.loading_label.hide()
        self.btn_refresh.setEnabled(True)
        self.btn_refresh.setText("Refresh")
        
        QtWidgets.QMessageBox.critical(
            self, 
            "Error Loading History", 
            f"Failed to load upload history:\n{error_msg}"
        )

    def closeEvent(self, event):
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        event.accept()
