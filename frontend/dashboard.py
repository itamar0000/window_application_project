from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QTableWidget, QTableWidgetItem, QFrame, QGridLayout, QHeaderView)
from PySide6.QtCharts import QChart, QChartView, QLineSeries
from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QPainter
import sys
from datetime import datetime, timedelta

class StyleSheet:
    MAIN_STYLE = """
        QMainWindow {
            background-color: #f5f6fa;
        }
        QWidget {
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        QLabel {
            color: #2c3e50;
            font-size: 14px;
        }
        QLineEdit {
            padding: 8px;
            border: 2px solid #dcdde1;
            border-radius: 4px;
            background-color: white;
            font-size: 14px;
            color: #2c3e50;
        }
        QLineEdit:focus {
            border: 2px solid #3498db;
        }
        QPushButton {
            background-color: #3498db;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QPushButton:pressed {
            background-color: #2471a3;
        }
        QTableWidget {
            background-color: white;
            border: 1px solid #dcdde1;
            border-radius: 4px;
            gridline-color: #f1f2f6;
        }
        QTableWidget::item {
            padding: 5px;
        }
        QTableWidget::item:selected {
            background-color: #3498db;
            color: white;
        }
        QHeaderView::section {
            background-color: #f8f9fa;
            padding: 8px;
            border: none;
            border-right: 1px solid #dcdde1;
            font-weight: bold;
            color: #2c3e50;
        }
    """


class PortfolioView(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_portfolio_data()

    def setup_ui(self):
        layout = QGridLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Portfolio Summary
        summary_card = self.create_summary_card()
        layout.addWidget(summary_card, 0, 0, 1, 2)

        # Holdings Table
        table_card = self.create_table_card()
        layout.addWidget(table_card, 1, 0, 1, 1)

        # Portfolio Performance Chart
        chart_card = self.create_chart_card()
        layout.addWidget(chart_card, 1, 1, 1, 1)

        # Trading Controls
        trading_card = self.create_trading_card()
        layout.addWidget(trading_card, 2, 0, 1, 2)

        self.setLayout(layout)

    def create_summary_card(self):
        summary_card = QFrame()
        summary_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        summary_layout = QHBoxLayout()

        # Total Value
        value_container = QFrame()
        value_layout = QVBoxLayout()
        value_label = QLabel("Total Portfolio Value")
        value_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        self.total_value_label = QLabel("$0.00")
        self.total_value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        value_layout.addWidget(value_label)
        value_layout.addWidget(self.total_value_label)
        value_container.setLayout(value_layout)

        # Daily Change
        change_container = QFrame()
        change_layout = QVBoxLayout()
        change_label = QLabel("Daily Change")
        change_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        self.daily_change_label = QLabel("$0.00 (0.00%)")
        self.daily_change_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #27ae60;")
        change_layout.addWidget(change_label)
        change_layout.addWidget(self.daily_change_label)
        change_container.setLayout(change_layout)

        summary_layout.addWidget(value_container)
        summary_layout.addWidget(change_container)
        summary_card.setLayout(summary_layout)

        return summary_card

    def create_table_card(self):
        table_card = QFrame()
        table_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        table_layout = QVBoxLayout()

        table_title = QLabel("Holdings")
        table_title.setStyleSheet("font-size: 18px; font-weight: bold; color: Black;")

        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(5)
        self.stock_table.setHorizontalHeaderLabels([
            "Symbol", "Shares", "Current Price", "Value", "Daily Change %"
        ])
        self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table_layout.addWidget(table_title)
        table_layout.addWidget(self.stock_table)
        table_card.setLayout(table_layout)

        return table_card

    def create_chart_card(self):
        chart_card = QFrame()
        chart_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        chart_layout = QVBoxLayout()
        chart_title = QLabel("Portfolio Performance")
        chart_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        self.chart_view = self.create_chart()
        chart_layout.addWidget(chart_title)
        chart_layout.addWidget(self.chart_view)
        chart_card.setLayout(chart_layout)

        return chart_card

    def create_trading_card(self):
        trading_card = QFrame()
        trading_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        trading_layout = QVBoxLayout()
        trading_title = QLabel("Trade")
        trading_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")

        controls_layout = QHBoxLayout()
        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("Stock Symbol")
        self.shares_input = QLineEdit()
        self.shares_input.setPlaceholderText("Number of Shares")

        buy_button = QPushButton("Buy")
        buy_button.setStyleSheet("background-color: #27ae60;")
        buy_button.clicked.connect(self.handle_buy)

        sell_button = QPushButton("Sell")
        sell_button.setStyleSheet("background-color: #e74c3c;")
        sell_button.clicked.connect(self.handle_sell)

        controls_layout.addWidget(self.symbol_input)
        controls_layout.addWidget(self.shares_input)
        controls_layout.addWidget(buy_button)
        controls_layout.addWidget(sell_button)

        trading_layout.addWidget(trading_title)
        trading_layout.addLayout(controls_layout)
        trading_card.setLayout(trading_layout)

        return trading_card

    def create_chart(self):
        chart = QChart()
        chart.setTitle("")
        chart.setTheme(QChart.ChartThemeLight)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        series = QLineSeries()
        series.setColor(QColor("#3498db"))

        for i in range(30):
            date = datetime.now() - timedelta(days=i)
            value = 10000 + (i * 100)
            series.append(QPointF(i, value))

        chart.addSeries(series)
        chart.createDefaultAxes()

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setMinimumHeight(300)
        return chart_view

    def load_portfolio_data(self):
        sample_data = [
            ("AAPL", 10, 150.00),
            ("GOOGL", 5, 2800.00),
            ("MSFT", 15, 280.00)
        ]

        self.stock_table.setRowCount(len(sample_data))
        total_value = 0

        for row, (symbol, shares, price) in enumerate(sample_data):
            value = shares * price
            total_value += value

            self.stock_table.setItem(row, 0, QTableWidgetItem(symbol))
            self.stock_table.setItem(row, 1, QTableWidgetItem(str(shares)))
            self.stock_table.setItem(row, 2, QTableWidgetItem(f"${price:,.2f}"))
            self.stock_table.setItem(row, 3, QTableWidgetItem(f"${value:,.2f}"))
            self.stock_table.setItem(row, 4, QTableWidgetItem("0.00%"))

        self.total_value_label.setText(f"${total_value:,.2f}")

    def handle_buy(self):
        symbol = self.symbol_input.text().upper()
        try:
            shares = int(self.shares_input.text())
            print(f"Buying {shares} shares of {symbol}")
        except ValueError:
            print("Invalid number of shares")

    def handle_sell(self):
        symbol = self.symbol_input.text().upper()
        try:
            shares = int(self.shares_input.text())
            print(f"Selling {shares} shares of {symbol}")
        except ValueError:
            print("Invalid number of shares")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Portfolio Manager")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(StyleSheet.MAIN_STYLE)

        self.portfolio_view = PortfolioView()
        self.setCentralWidget(self.portfolio_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
