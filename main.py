from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox
from PyQt5.QtCore import QFile
from PyQt5.uic import loadUi
import sys
import requests
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI file
        ui_file = QFile("design.ui")
        ui_file.open(QFile.ReadOnly)
        loadUi(ui_file, self)
        ui_file.close()

        self.weather = 0
        self.label_2.setText(f"{self.weather_parse()}°C")

        # Access the QComboBox
        self.combobox = self.findChild(QComboBox, "comboBox")
        self.combobox_2 = self.findChild(QComboBox, "comboBox_2")

        # Connect the signal of QComboBox
        self.combobox.currentIndexChanged.connect(self.on_combobox_index_changed)
        self.combobox_2.currentIndexChanged.connect(self.on_combobox_index_changed)


    def weather_parse(self):
        BASE_URL = "http://api.openweathermap.org/data/2.5/weather?q=Almaty,kz&APPID="
        api_key = "1e5cfaa68edd16109cd1c6c03c764fab"
        url = BASE_URL + api_key
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            main = data['main']
            temperature = int(main["temp"] - 273.15)
            return temperature
        else:
            print('Error')
            return None

    def on_combobox_index_changed(self, index):
        url = "https://api.bcc.kz/bcc/production/v1/auth/RatesArray"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print('Error')
            return None

        selected_item = self.combobox.currentText()

        print("Selected item:", selected_item)



app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
