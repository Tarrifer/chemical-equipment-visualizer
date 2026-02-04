import sys
import os
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtGui import QIcon
from api import upload_csv, download_pdf, set_token
from login import LoginDialog
from history import HistoryDialog

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class UploadWorker(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
    
    def run(self):
        try:
            data = upload_csv(self.file_path)
            self.finished.emit(data)
        except Exception as e:
            self.error.emit(str(e))


class DownloadWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, save_path):
        super().__init__()
        self.save_path = save_path
    
    def run(self):
        try:
            download_pdf(self.save_path)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi(resource_path("ui/main_window.ui"), self)

        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))
        self.lbl_total.setText("Total Equipment: -")
        self.lbl_flowrate.setText("Average Flowrate: -")
        self.lbl_pressure.setText("Average Pressure: -")
        self.lbl_temperature.setText("Average Temperature: -")
        self.lbl_distribution.setText(
            "Equipment Type Distribution: Upload a CSV file to see results"
        )

        self.btn_upload.clicked.connect(self.handle_upload)
        self.btn_pdf.clicked.connect(self.handle_download_pdf)
        self.btn_logout.clicked.connect(self.handle_logout)
        self.btn_history.clicked.connect(self.open_history)

        self.centralwidget.layout().setContentsMargins(20, 20, 20, 20)
        self.centralwidget.layout().setSpacing(15)

        self.figure = Figure(figsize=(8, 4), dpi=100)
        self.figure.patch.set_facecolor('#ffffff')
        self.canvas = FigureCanvas(self.figure)
        layout = QtWidgets.QVBoxLayout(self.chartFrame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        
        self.upload_worker = None
        self.download_worker = None
        
        self.center_on_screen()

    def center_on_screen(self):
        qt_rectangle = self.frameGeometry()
        center_point = QtWidgets.QApplication.desktop().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def handle_upload(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        if not file_path:
            return

        self.btn_upload.setEnabled(False)
        self.btn_upload.setText("Uploading...")
        
        self.upload_worker = UploadWorker(file_path)
        self.upload_worker.finished.connect(self.on_upload_success)
        self.upload_worker.error.connect(self.on_upload_error)
        self.upload_worker.start()

    def on_upload_success(self, data):
        try:
            self.lbl_total.setText(f"Total Equipment: {data['total_equipment']}")
            self.lbl_flowrate.setText(f"Average Flowrate: {data['average_flowrate']:.2f}")
            self.lbl_pressure.setText(f"Average Pressure: {data['average_pressure']:.2f}")
            self.lbl_temperature.setText(f"Average Temperature: {data['average_temperature']:.2f}")

            dist = data["equipment_type_distribution"]
            self.lbl_distribution.setText(
                "Equipment Type Distribution: " +
                ", ".join(f"{k}: {v}" for k, v in dist.items())
            )

            self.draw_chart(dist)
            
            QMessageBox.information(self, "Success", "CSV file uploaded and processed successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error processing data: {str(e)}")
        finally:
            self.btn_upload.setEnabled(True)
            self.btn_upload.setText("Upload CSV File")

    def on_upload_error(self, error_msg):
        QMessageBox.critical(self, "Upload Error", f"Failed to upload file:\n{error_msg}")
        self.btn_upload.setEnabled(True)
        self.btn_upload.setText("Upload CSV File")

    def draw_chart(self, distribution):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        types = list(distribution.keys())
        counts = list(distribution.values())

        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6', 
                  '#1abc9c', '#34495e', '#e67e22', '#95a5a6', '#d35400']
        colors = colors[:len(types)]
        
        bars = ax.bar(types, counts, color=colors, edgecolor='white', linewidth=1.5)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')

        ax.set_title("Equipment Type Distribution", fontsize=14, fontweight='bold', pad=15)
        ax.set_ylabel("Count", fontsize=11, fontweight='600')
        ax.set_xlabel("Equipment Type", fontsize=11, fontweight='600')
        ax.tick_params(axis='x', rotation=45, labelsize=9)
        ax.tick_params(axis='y', labelsize=9)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        self.figure.tight_layout()
        self.canvas.draw()

    def handle_download_pdf(self):
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF", "equipment_report.pdf", "PDF Files (*.pdf)"
        )
        if not save_path:
            return

        self.btn_pdf.setEnabled(False)
        self.btn_pdf.setText("Downloading...")
        
        self.download_worker = DownloadWorker(save_path)
        self.download_worker.finished.connect(self.on_download_success)
        self.download_worker.error.connect(self.on_download_error)
        self.download_worker.start()

    def on_download_success(self):
        QMessageBox.information(self, "Success", "PDF report downloaded successfully!")
        self.btn_pdf.setEnabled(True)
        self.btn_pdf.setText("Download PDF Report")

    def on_download_error(self, error_msg):
        QMessageBox.critical(self, "Download Error", f"Failed to download PDF:\n{error_msg}")
        self.btn_pdf.setEnabled(True)
        self.btn_pdf.setText("Download PDF Report")

    def handle_logout(self):
        reply = QMessageBox.question(
            self, 'Confirm Logout', 
            'Are you sure you want to logout?',
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
            
        set_token(None)
        self.close()

        login_dialog = LoginDialog()
        if login_dialog.exec_() != QtWidgets.QDialog.Accepted:
            sys.exit(0)

        new_window = MainWindow()
        new_window.show()

    def open_history(self):
        dialog = HistoryDialog(self)
        dialog.exec_()

    def closeEvent(self, event):
        if self.upload_worker and self.upload_worker.isRunning():
            self.upload_worker.terminate()
            self.upload_worker.wait()
        
        if self.download_worker and self.download_worker.isRunning():
            self.download_worker.terminate()
            self.download_worker.wait()
        
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("assets/icon.ico")))

    app.setStyle('Fusion')

    login = LoginDialog()
    if login.exec_() != QtWidgets.QDialog.Accepted:
        sys.exit(0)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
