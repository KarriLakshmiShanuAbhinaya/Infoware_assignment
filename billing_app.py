import sys
import mysql.connector
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)

class BillingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Billing Application")
        self.setGeometry(200, 200, 600, 400)
        
        # Set minimum window size to prevent it from getting too small
        self.setMinimumSize(600, 350)

        self.initUI()
        self.connect_db()

    def initUI(self):
        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout()


        # Customer Form
        self.customer_name_label = QLabel("Customer Name")
        self.customer_name_input = QLineEdit()

        self.customer_address_label = QLabel("Customer Address")
        self.customer_address_input = QLineEdit()

        self.product_desc_label = QLabel("Product Description")
        self.product_desc_input = QLineEdit()

        self.quantity_label = QLabel("Quantity")
        self.quantity_input = QLineEdit()

        self.price_label = QLabel("Price")
        self.price_input = QLineEdit()

        # Total Amount (calculated automatically)
        self.total_label = QLabel("Total Amount (Calculated)")
        self.total_output = QLabel("")

        self.save_button = QPushButton("Save Details")
        self.save_button.clicked.connect(self.save_bill)

        self.retrieve_button = QPushButton("Retrieve Details")
        self.retrieve_button.clicked.connect(self.show_search_bar)

        # Search bar for Bill ID and Enter button
        self.bill_id_input = QLineEdit()
        self.bill_id_input.setPlaceholderText("Enter Bill ID")
        self.bill_id_input.setVisible(False)  # Initially hidden

        self.enter_button = QPushButton("Enter")
        self.enter_button.setVisible(False)  # Initially hidden
        self.enter_button.clicked.connect(self.retrieve_bill_by_id)

        

        layout.addWidget(self.customer_name_label)
        layout.addWidget(self.customer_name_input)

        layout.addWidget(self.customer_address_label)
        layout.addWidget(self.customer_address_input)

        layout.addWidget(self.product_desc_label)
        layout.addWidget(self.product_desc_input)

        layout.addWidget(self.quantity_label)
        layout.addWidget(self.quantity_input)

        layout.addWidget(self.price_label)
        layout.addWidget(self.price_input)

        layout.addWidget(self.total_label)
        layout.addWidget(self.total_output)

        layout.addWidget(self.save_button)

        layout.addWidget(self.retrieve_button)
        layout.addWidget(self.bill_id_input)
        layout.addWidget(self.enter_button)

        # Table to display stored bills
        self.table = QTableWidget()
        layout.addWidget(self.table)

        widget.setLayout(layout)

    def connect_db(self):
        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Abhinaya@123",
                database="Info"
            )
            self.cursor = self.db_connection.cursor()
            print("Connected to database")
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error connecting to database: {err}")
            sys.exit(1)

    def save_bill(self):
        name = self.customer_name_input.text()
        address = self.customer_address_input.text()
        product = self.product_desc_input.text()
        quantity = self.quantity_input.text()
        price = self.price_input.text()

        if not name or not address or not product or not quantity or not price:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields")
            return

        try:
            # Calculate total amount automatically
            total = int(quantity) * float(price)

            # Insert customer data
            self.cursor.execute("INSERT INTO Customer (name, address) VALUES (%s, %s)", (name, address))
            customer_id = self.cursor.lastrowid

            # Insert bill data
            self.cursor.execute(
                "INSERT INTO Bill (customer_id, product_description, quantity, price, total_amount) "
                "VALUES (%s, %s, %s, %s, %s)",
                (customer_id, product, int(quantity), float(price), total)
            )

            self.db_connection.commit()

            # Get the generated bill_id
            bill_id = self.cursor.lastrowid
            QMessageBox.information(self, "Success", f"Bill saved successfully! Bill ID: {bill_id}")

            self.total_output.setText(str(total))

            # Adjust the window size after saving
            self.adjustSize()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error saving bill: {err}")
        finally:
            self.clear_inputs()

    def show_search_bar(self):
        # Show search bar and Enter button for Bill ID retrieval
        self.bill_id_input.setVisible(True)
        self.enter_button.setVisible(True)

    def retrieve_bill_by_id(self):
        bill_id = self.bill_id_input.text()
        if not bill_id:
            QMessageBox.warning(self, "Input Error", "Please enter a Bill ID")
            return

        try:
            # Retrieve bill and customer information by bill_id
            self.cursor.execute(
                "SELECT Bill.bill_id, Customer.name, Customer.address, Bill.product_description, Bill.quantity, Bill.price, Bill.total_amount "
                "FROM Bill JOIN Customer ON Bill.customer_id = Customer.customer_id WHERE Bill.bill_id = %s", (bill_id,)
            )
            row = self.cursor.fetchone()

            if row:
                # Update fields with retrieved data
                self.customer_name_input.setText(row[1])
                self.customer_address_input.setText(row[2])
                self.product_desc_input.setText(row[3])
                self.quantity_input.setText(str(row[4]))
                self.price_input.setText(str(row[5]))

                # Update total amount field
                self.total_output.setText(str(row[6]))

                # Display bill details in table
                self.table.setRowCount(0)  # Clear previous data
                self.table.setColumnCount(7)
                self.table.setHorizontalHeaderLabels(
                    ["Bill ID", "Customer Name", "Address", "Product", "Quantity", "Price", "Total Amount"]
                )

                self.table.insertRow(0)
                for col_index, data in enumerate(row):
                    self.table.setItem(0, col_index, QTableWidgetItem(str(data)))

                # Adjust the window size after retrieval
                self.adjustSize()

            else:
                QMessageBox.information(self, "Not Found", f"No bill found with ID: {bill_id}")

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error", f"Error retrieving bill: {err}")

    def clear_inputs(self):
        self.customer_name_input.clear()
        self.customer_address_input.clear()
        self.product_desc_input.clear()
        self.quantity_input.clear()
        self.price_input.clear()
        self.total_output.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = BillingApp()
    mainWindow.show()

    sys.exit(app.exec())
