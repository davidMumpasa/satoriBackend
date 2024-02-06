from flask import Flask, request, jsonify
from flask_cors import CORS
from models.user import db
from flask_bcrypt import Bcrypt
from models.user import UserModel, db

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:DavidEbula1999@localhost:3306/taskpro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BCRYPT_LOG_ROUNDS'] = 12

bcrypt = Bcrypt(app)
db.init_app(app)

with app.app_context():
    db.create_all()

from businesslogic import storeUser  # Updated import statement

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        # Check if all required fields are present in the request
        required_fields = ['email', 'password']
        if not all(field in data for field in required_fields):
            raise ValueError('Missing required fields')

        email = data['email']
        password = data['password']

        user = UserModel.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return jsonify({'message': 'Login successful'}), 200
        else:
            raise ValueError('Invalid credentials')

    except ValueError as e:
        return jsonify({'error': str(e)}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/register', methods=['POST'])
def registration():
    try:
        # Extract information from the request and store user
        user_data = storeUser() 

        return jsonify({'user': user_data}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
