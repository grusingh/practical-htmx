# Project Description

This project is a simple product management system built with Python and Flask. It provides a web interface for managing a list of products, each with properties such as name, description, price, stock, and an archive status. The system supports basic CRUD operations (Create, Read, Update, Delete) on the products. It also includes a feature to visualize the stock of products in a bar chart and endpoints to get the total stock in plain text and JSON format.

# Project Structure

The project mainly consists of a single Python file `app.py` and two HTML templates `base.html` and `product_edit.html`.

- `app.py`: This is the main application file where the Flask app is defined and all the routes are set up. It also includes the in-memory storage for products and the functions for validating product data and calculating total stock.

- `base.html`: This is the base HTML template that includes the basic structure of the HTML pages.

- `product_edit.html`: This is the HTML template for the product edit form.

# Setup Instructions

To set up and run this project, follow the steps below:

1. Ensure that you have Python installed on your system. You can verify this by running `python --version` in your terminal. If you don't have Python installed, you can download it from the official website.

2. Clone the project repository to your local machine using the command `git clone https://github.com/grusingh/practical-htmx.git`.

3. Navigate to the project directory using the command `cd practical-htmx`.

4. Install the required Python packages using pip. Run the command `pip install -r requirements.txt`.

5. Run the Flask application with the command `python app.py`.

After following these steps, the Flask server should be up and running. You can access the web interface by opening your web browser and navigating to `http://localhost:5000/`.