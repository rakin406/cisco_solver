from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CISCO Solver")
        self.setFixedSize(QSize(700, 600))

        layout = QVBoxLayout()

        # Create button
        button = QPushButton("Start")
        button.setFixedSize(QSize(200, 100))
        button.setFont(QFont("Arial", 20))
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(widget)


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
