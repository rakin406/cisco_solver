import threading

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont

from solver import Solver


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CISCO Solver")
        self.setFixedSize(QSize(700, 600))
        self.solver = Solver()

        layout = QVBoxLayout()

        # Create button
        self.button = QPushButton("Start")
        self.button.setFixedSize(QSize(200, 100))
        self.button.setFont(QFont("Arial", 20))
        self.button.setCheckable(True)
        self.button.toggled.connect(self.on_button_toggled)
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(widget)

    def on_button_toggled(self, checked):
        if checked:
            self.button.setText("Stop")
            thread = threading.Thread(target=self.solver.start)
            thread.start()
        else:
            self.button.setText("Start")
            self.solver.stop()


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
