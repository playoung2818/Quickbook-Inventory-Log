# QuickBook Inventory Log

## Overview

The QuickBook Inventory Log is a web application that reads through an Excel file of inventory status downloaded from QuickBook, automatically creating sub-pages for each product group, allowing for better organization and quick access to specific inventory details.

## Screenshot

![image](https://github.com/user-attachments/assets/859bd96a-0d8e-4285-8b02-57c9c331de63)

![image](https://github.com/user-attachments/assets/388cda4c-06d3-446b-8890-24af04215ebf)


![image](https://github.com/user-attachments/assets/aea5e051-cf86-4586-a116-db12ac19fbf7)

## Key Features

- **Excel File Parsing:** The application reads and processes an Excel file exported from QuickBook, extracting inventory data and organizing it by product group.
  
- **Dynamic Sub-Pages:** For each product group identified in the Excel file, the application dynamically generates a dedicated sub-page. These sub-pages provide a detailed view of the inventory status, making it easy to monitor stock levels and manage inventory.

- **Fuzzy Search Bar:** This feature allows users to quickly find items within the inventory by typing related keywords, significantly speeding up the search process and improving user experience by tolerating minor typos and variations in item names.

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
