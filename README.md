PySide Billing Application
This project is a Python-based desktop billing application built using PySide for the graphical interface and MySQL for the database. The application allows users to create bills, store them in a local MySQL database, and retrieve previously stored bills using a bill ID.

Features
Create and save bills: Users can enter customer details, product name, quantity, and price to generate and save bills.
Dynamic Bill ID generation: The Bill ID is automatically generated after saving the details.
Retrieve bill details: Users can retrieve bill details by entering the generated Bill ID.
Responsive window: The application size dynamically adjusts based on the number of details entered.
Prerequisites
Make sure you have the following before running the project:

Python 3.x
MySQL Server
Required Python libraries:
PySide6
MySQL connector for Python (mysql-connector-python)
Database Setup
You need to create a MySQL database and two tables: one for storing customer information and one for storing bill details.

Customer Table: Stores information such as customer ID, name, and contact number.
Bill Table: Stores information related to each bill, including bill ID, product name, quantity, price, and total amount. It also links to the Customer table via a foreign key.
The tables are linked through the customer_id, and the application ensures referential integrity between customers and their bills.

Steps to Set Up the Database:
Create a new MySQL database.
Define the necessary tables for Customer and Bill.
Ensure that foreign key constraints are applied between the tables to link customer details with their bills.
How to Run the Application
Install the required dependencies using Python's package manager (pip).
Clone this repository and navigate to the project folder.
Run the main Python script to launch the application.
Application Workflow
1. Saving Bill Details:
Enter the customer details (name and contact number), product name, quantity, and price.
Once the details are entered, click the "Save Details" button to generate a Bill ID and save the bill in the database.
The generated Bill ID will be displayed after saving.
2. Retrieving Bill Details:
Click the "Retrieve Details" button.
Enter the Bill ID to retrieve and display the saved details, including customer information, product, and total amount.
A search bar is available below the retrieve details button for entering the Bill ID.
