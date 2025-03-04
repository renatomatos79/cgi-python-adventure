from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Import the config class
from config import config_class

app = Flask(__name__)

# Load configurations from config.py
app.config.from_object(config_class)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Initialize Database
with app.app_context():
    db.create_all()

# Create (POST)
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(name=data['name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created!"}), 201

# Read (GET)
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "name": user.name} for user in users])

# Read by ID (GET)
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify({"id": user.id, "name": user.name})
    return jsonify({"message": "User not found"}), 404

# Update (PUT)
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if user:
        data = request.json
        user.name = data['name']
        db.session.commit()
        return jsonify({"message": "User updated!"})
    return jsonify({"message": "User not found"}), 404

# Delete (DELETE)
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted!"})
    return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    if config_class.DEBUG:
        app.run(debug=True, port=config_class.PORT)
    else:
        print(f"Running without debug mode PORT: {config_class.PORT}")
        from waitress import serve
        serve(app, host="0.0.0.0", port=config_class.PORT)
