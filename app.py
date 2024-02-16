from datetime import datetime
from flask import Flask, request, render_template, redirect, abort, send_file, jsonify
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

# In-memory storage for products
products = [
    {"id": 1, "name": "Laptop",
     "description": "High-performance laptop ideal for gaming and professional tasks, featuring a high-resolution display and long battery life.",
     "price": 77.73, "archived": False, "updated_at": "2022-08-12", "stock": 33},
    {"id": 2, "name": "Desktop PC",
     "description": "Powerful desktop PC with the latest CPU and GPU, designed for gaming, video editing, and software development.",
     "price": 891.25, "archived": False, "updated_at": "2023-04-02", "stock": 99},
    {"id": 3, "name": "Gaming Mouse",
     "description": "Ergonomic gaming mouse with customizable RGB lighting, adjustable DPI settings, and programmable buttons.",
     "price": 504.3, "archived": False, "updated_at": "2022-02-14", "stock": 62},
    {"id": 4, "name": "Mechanical Keyboard",
     "description": "Durable mechanical keyboard with tactile switches, RGB backlighting, and anti-ghosting keys for precise typing and gaming.",
     "price": 905.1, "archived": True, "updated_at": "2023-08-29", "stock": 91},
    {"id": 5, "name": "Monitor",
     "description": "Ultra-wide monitor with stunning resolution, fast refresh rate, and low latency, perfect for gaming and professional design work.",
     "price": 488.47, "archived": False, "updated_at": "2023-02-01", "stock": 50},
    {"id": 6, "name": "Graphics Card",
     "description": "Top-of-the-line graphics card offering unparalleled performance for gaming and rendering, supporting 4K and ray tracing.",
     "price": 131.64, "archived": False, "updated_at": "2022-12-02", "stock": 28},
    {"id": 7, "name": "SSD Drive",
     "description": "Fast SSD drive with high storage capacity, improving boot times and speeding up application loading and file transfers.",
     "price": 157.37, "archived": False, "updated_at": "2023-06-21", "stock": 64},
    {"id": 8, "name": "External Hard Drive",
     "description": "Portable external hard drive with ample storage space for backups, media, and files, featuring USB 3.0 connectivity.",
     "price": 634.18, "archived": True, "updated_at": "2022-05-06", "stock": 59},
    {"id": 9, "name": "Webcam",
     "description": "High-definition webcam with clear audio capture, perfect for video conferencing, streaming, and online classes.",
     "price": 870.52, "archived": True, "updated_at": "2022-06-06", "stock": 91},
    {"id": 10, "name": "USB Cable",
     "description": "Durable USB cable supporting fast charging and high-speed data transfer, compatible with various devices.",
     "price": 61.79, "archived": False, "updated_at": "2022-06-09", "stock": 51}
]


def validate_product(form_data):
    errors = {}
    required_fields = ['name', 'description', 'price', 'stock']
    for field in required_fields:
        if field not in form_data:
            errors[field] = f"{field} is required"
        elif field == 'name' or field == 'description':
            if len(form_data[field]) < 3:
                errors[field] = f"{field} must be at least 3 characters long"
        elif field == 'price' or field == 'stock':
            try:
                float(form_data[field])
            except ValueError:
                errors[field] = f"{field} must be a number"
    return errors


def get_total_stock():
    return sum(product['stock'] for product in products)


@app.route('/', methods=['GET'])
def get_products():
    return render_template('index.html', products=products, edit_product_id=None, values=None, errors=None,
                           total_stock="-")


@app.route('/products/create', methods=['POST'])
def post_product():
    form_data = request.form.to_dict()
    errors = validate_product(form_data)

    if errors:
        return render_template('index.html', products=products, edit_product_id=None, values=form_data,
                               errors=errors, total_stock=get_total_stock()), 400

    form_data['updated_at'] = datetime.utcnow().date().strftime("%Y-%m-%d")
    products.append(form_data)
    return redirect('/')


@app.route('/products/<int:product_id>/put', methods=['POST'])
def put_product(product_id):
    for product in products:
        if product['id'] == product_id:
            form_data = request.form.to_dict()
            errors = validate_product(form_data)

            if errors:
                return render_template('index.html', products=products, edit_product_id=product_id, values=form_data,
                                       errors=errors, total_stock=get_total_stock()), 400

            form_data['updated_at'] = datetime.utcnow().date().strftime("%Y-%m-%d")
            product.update(form_data)
            return redirect('/')
    abort(404)


@app.route('/products/<int:product_id>/patch', methods=['POST'])
def archive_product(product_id):
    for product in products:
        if product['id'] == product_id:
            product['archived'] = request.form.get('archived').lower() == 'true'
            product['updated_at'] = datetime.utcnow().date().strftime("%Y-%m-%d")
            return redirect('/')
    abort(404)


@app.route('/products/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    for product in products:
        if product['id'] == product_id:
            products.remove(product)
            return redirect('/')
    abort(404)


@app.route('/products/<int:product_id>/edit', methods=['GET'])
def edit_product(product_id):
    return render_template('index.html', products=products, edit_product_id=product_id, values=None, errors=None,
                           total_stock=get_total_stock())


@app.route('/products/stock_chart', methods=['GET'])
def stock_chart():
    # Create a new figure and an axis
    fig, ax = plt.subplots()

    # Get the product names and their stocks
    product_names = [product['name'] for product in products]
    product_stocks = [product['stock'] for product in products]

    # Plot the product stocks
    ax.bar(product_names, product_stocks)
    ax.set_xlabel('Product')
    ax.set_ylabel('Stock')
    ax.set_title('Product Stock Chart')

    # Save the figure to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Return the BytesIO object as an image file
    return send_file(img, mimetype='image/png')


@app.route('/products/total_stock', methods=['GET'])
def total_stock():
    # Calculate the total stock
    total = sum(product['stock'] for product in products)

    # Return the total stock as a string
    return str(total)


@app.route('/products/total_stock_json', methods=['GET'])
def total_stock_json():
    # Calculate the total stock
    total = sum(product['stock'] for product in products)
    data = {"total_stock": total}

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
