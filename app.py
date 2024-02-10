from flask import Flask, request, render_template, jsonify
from flask.views import MethodView

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


@app.route('/', methods=['GET'])
def get_products():
    return render_template('index.html', products=products, edit_product_id=None)


@app.route('/products/', methods=['POST'])
def post_product():
    new_product = request.json
    new_product['id'] = len(products) + 1
    products.append(new_product)
    return jsonify(new_product), 201


@app.route('/products/<int:product_id>', methods=['PUT'])
def put_product(product_id):
    for product in products:
        if product['id'] == product_id:
            product.update(request.json)
            return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    for product in products:
        if product['id'] == product_id:
            products.remove(product)
            return jsonify({"success": True}), 200
    return jsonify({"error": "Product not found"}), 404


@app.route('/product/<int:product_id>/edit', methods=['GET'])
def edit_product(product_id):
    return render_template('index.html', products=products, edit_product_id=product_id)


if __name__ == '__main__':
    app.run(debug=True)
