import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QDialog,
    QFormLayout,
    QLineEdit,
    QDialogButtonBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import generations

class MatplotlibWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

        # self.plot()

    def plot(self, game: generations.Game):
        game.next_iteration()
        generations.show_grid(game.get_current_iteration())

class ParameterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Enter Parameters')
        self.layout = QFormLayout()

        self.ALineEdit = QLineEdit()
        self.BLineEdit = QLineEdit()
        self.CLineEdit = QLineEdit()
        self.DLineEdit = QLineEdit()
        self.ELineEdit = QLineEdit()

        self.layout.addRow('Rule S:', self.ALineEdit)
        self.layout.addRow('Rule B:', self.BLineEdit)
        self.layout.addRow('Rule C:', self.CLineEdit)
        self.layout.addRow('Size of the grid:', self.DLineEdit)
        self.layout.addRow('Alive cells:', self.ELineEdit)


        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            parent=self
        )
        self.layout.addRow(self.buttons)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.setLayout(self.layout)

    def get_parameters(self):
        A = [int(i) for i in self.ALineEdit.text().split(",")]
        B = [int(i) for i in self.ALineEdit.text().split(",")]
        C = int(self.CLineEdit.text())
        D = int(self.DLineEdit.text())
        E = [int(i) for i in self.ELineEdit.text().split(",")]
        return A, B, C, D, E

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = MatplotlibWidget()
        self.setCentralWidget(self.central_widget)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Generations')
        self.game = generations.Game(50, [2], [2], 25, [1224, 1274, 1275])
        self.param_dialog = None
        self.create_button()
        self.create_button2()
        self.show()

    def create_button(self):
        button = QPushButton('Create the Game', self)
        button.clicked.connect(lambda: self.show_parameter_dialog)

    def create_button2(self):
        button2 = QPushButton('Next iteration', self)
        button2.clicked.connect(lambda: self.central_widget.plot(self.game))
    
    def show_parameter_dialog(self):
        if not self.param_dialog:
            self.param_dialog = ParameterDialog(self)

        result = self.param_dialog.exec_()
        if result == QDialog.Accepted:
            A, B, C, D, E = self.param_dialog.get_parameters()
            self.game = generations.Game(D, A, B, C, E)

def main():
    app = QApplication(sys.argv)
    window = MyApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
