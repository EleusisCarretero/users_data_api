from flask import Flask, jsonify
import random

app = Flask(__name__)

first_names = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Fernanda"]
last_names = ["Gomez", "Lopez", "Martinez", "Perez", "Rodriguez", "Sanchez"]
zip_codes = ["10001", "90210", "75001", "33101", "60601"]

@app.route('/')
def home():
    return jsonify({"message": "API de Contactos en Flask"})

@app.route('/contact', methods=['GET'])
def get_contact():
    return jsonify({
        "first_name": random.choice(first_names),
        "last_name": random.choice(last_names),
        "zip_code": random.choice(zip_codes)
    })

if __name__ == '__main__':
    app.run(debug=True)