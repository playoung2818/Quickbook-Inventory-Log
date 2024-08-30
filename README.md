# QuickBook Inventory Log

## Overview

The QuickBook Inventory Log is a web application that reads through an Excel file of inventory status downloaded from QuickBook, automatically creating sub-pages for each product group, allowing for better organization and quick access to specific inventory details.

## Screenshot
[
![image (1)](https://github.com/user-attachments/assets/b780b3b2-980c-44ab-8536-6c66c4f42842)
](url)

![image](https://github.com/user-attachments/assets/dbf9cdc0-77b9-4614-b88c-10a5262ac922)

![image](https://github.com/user-attachments/assets/aea5e051-cf86-4586-a116-db12ac19fbf7)

## Key Features

- **Excel File Parsing:** The application reads and processes an Excel file exported from QuickBook, extracting inventory data and organizing it by product group.
  
- **Dynamic Sub-Pages:** For each product group identified in the Excel file, the application dynamically generates a dedicated sub-page. These sub-pages provide a detailed view of the inventory status, making it easy to monitor stock levels and manage inventory.

- **Logging Functionality:** The application includes a logging feature, which provides users with a convenient tool for recording inventory counts. This function ensures that all inventory updates are documented accurately and efficiently, reducing the risk of errors and improving inventory accuracy.

## Getting Started

1. **Prerequisites:**
   - Python
   - Flask
   - Pandas
   - OpenPyXL

2. **Installation:**
   Clone the repository and install the required packages:
   ```bash
   git clone https://github.com/your-repository/quickbook-inventory-log.git
   cd quickbook-inventory-log
   pip install -r requirements.txt
