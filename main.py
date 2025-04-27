from PySide6.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout,
    QWidget, QLineEdit, QTableWidget, QTableWidgetItem
)
import mysql.connector

# --- Connect to MySQL ---
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="billo2002",  # <-- Apna password daalo
    database="form"
)
cursor = conn.cursor()

# --- PySide App Start ---
app = QApplication([])

# --- Widgets ---
phone_input = QLineEdit()
phone_input.setPlaceholderText("Phone Number")

name_input = QLineEdit()
name_input.setPlaceholderText("Customer Name")

product_input = QLineEdit()
product_input.setPlaceholderText("Product Name")

price_input = QLineEdit()
price_input.setPlaceholderText("Price per item")

quantity_input = QLineEdit()
quantity_input.setPlaceholderText("Quantity")

save_button = QPushButton("Save Customer")
status_label = QLabel("Status: Waiting...")

table = QTableWidget()
table.setColumnCount(6)
table.setHorizontalHeaderLabels(["Phone", "Name", "Product", "Price", "Quantity", "Total"])

# --- Function to Save and Load Data ---
def save_customer():
    print("Button Clicked")  # DEBUG

    phone = phone_input.text()
    name = name_input.text()
    product = product_input.text()
    price = price_input.text()
    quantity = quantity_input.text()

    if phone and name and product and price and quantity:
        try:
            total = float(price) * int(quantity)
            cursor.execute(
                "INSERT INTO customers (phone, name, product, price, quantity, total) VALUES (%s, %s, %s, %s, %s, %s)",
                (phone, name, product, float(price), int(quantity), total)
            )
            conn.commit()

            status_label.setText("✅ Customer saved!")

            phone_input.clear()
            name_input.clear()
            product_input.clear()
            price_input.clear()
            quantity_input.clear()

            load_data()
        except Exception as e:
            status_label.setText("Error:" + str(e))
    else:
        status_label.setText("Please fill all fields.")

def load_data():
    cursor.execute("SELECT phone, name, product, price, quantity, total FROM customers ORDER BY id DESC")
    rows = cursor.fetchall()

    table.setRowCount(len(rows))
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            table.setItem(i, j, QTableWidgetItem(str(val)))

# ✅ Button Connection
save_button.clicked.connect(save_customer)

# --- Layouts ---
form_layout = QVBoxLayout()
form_layout.addWidget(phone_input)
form_layout.addWidget(name_input)
form_layout.addWidget(product_input)
form_layout.addWidget(price_input)
form_layout.addWidget(quantity_input)
form_layout.addWidget(save_button)
form_layout.addWidget(status_label)
form_layout.addWidget(table)

window = QWidget()
window.setWindowTitle("Customer Billing - PySide + MySQL")
window.setLayout(form_layout)
window.resize(700, 500)

# Table load on start
load_data()

window.show()
app.exec()
conn.close()
