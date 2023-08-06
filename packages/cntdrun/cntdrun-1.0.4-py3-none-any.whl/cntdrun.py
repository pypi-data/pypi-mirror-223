import sys
import argparse
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, Qt


class CountdownWindow(QMainWindow):
    def __init__(self, count, command, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ctndrun")
        self.setGeometry(0, 0, 250, 150)
        self.setStyleSheet(
            "border: 1px solid green; color: green; background-color: black;"
        )
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        screen = QApplication.desktop().screenGeometry()
        x = int((screen.width() - self.width()) / 2)
        y = int((screen.height() - self.height()) / 2)
        self.move(x, y)

        self.countdown_label = QLabel(self)
        self.countdown_label.setFont(QFont("Arial", 32))
        self.countdown_label.setGeometry(50, 20, 150, 50)
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet("border: 1px solid black;")

        self.close_button = QPushButton("close", self)
        self.close_button.setGeometry(100, 100, 50, 30)
        self.close_button.clicked.connect(self.close)

        self.countdown = count
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)

        self.command = command

        self.countdown_label.setText(str(self.countdown))

    def update_countdown(self):
        self.countdown -= 1
        self.countdown_label.setText(str(self.countdown))
        if self.countdown == 0:
            self.timer.stop()
            self.countdown_label.setText("over")

            if self.command:
                print("Executing command:", self.command)
                try:
                    result = subprocess.run(
                        self.command,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )
                    if result.returncode == 0:
                        print("Command executed successfully.")
                        print("Command output:")
                        print(result.stdout)
                    else:
                        print("Command execution failed.")
                        print("Error message:")
                        print(result.stderr)
                except Exception as e:
                    print("Error occurred while executing command:", e)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.close_button.click()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("count", type=int, help="Countdown time in seconds")
    parser.add_argument("command", type=str, help="Command to execute after countdown")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    window = CountdownWindow(args.count, args.command)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
