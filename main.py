from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox
from PyQt5.QtCore import QFile
from PyQt5.uic import loadUi
import sys
import requests
import yfinance as yf
import datetime as dt

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
        self.combobox_2.setEditable(True)
        self.list1 = ["Выбрать", "USD/KZT", "EUR/KZT", "RUB/KZT", "KZT/USD", "KZT/EUR", "KZT/RUB"]
        self.comboBox.addItems(self.list1)
        self.pushButton.clicked.connect(self.on_combobox_index_changed)
        self.pushButton_2.clicked.connect(self.tickerData)

        self.label_5.setText(f"{self.on_combobox_index_changed(index='')}")


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
        index = self.combobox.currentText()
        base_currency = index[:3]
        target_currency = index[4:]
        ticker = f"{base_currency}{target_currency}=X"
        start_date = dt.datetime.today() - dt.timedelta(days = 1)
        end_date = dt.datetime.today()
        data = yf.download(ticker, start_date, end_date)
        if data.empty:
            self.label_5.setText("No data available for the selected currency pair.")
        else:
            exchange_rate = data["Close"].iloc[0]
            self.label_5.setText(f"{exchange_rate}")

    def tickerData(self):
        ticker = self.combobox_2.currentText()
        start_date = dt.datetime.today() - dt.timedelta(days=1)
        end_date = dt.datetime.today()
        data = yf.download(ticker, start_date, end_date)
        if data.empty:
            print("No data available for the selected currency pair.")
        else:
            close_data = data["Close"]
            close_price = close_data.iloc[0]
            self.label_6.setText(str(close_price)) 

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())




