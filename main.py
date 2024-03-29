from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from businesslogic import storeUser
from models.user import UserModel,db

app = Flask(__name__)
CORS(app, supports_credentials=True)

app = Flask(__name__)
CORS(app, supports_credentials=True)
# logging.basicConfig(filename='app.log', level=logging.DEBUG)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:DavidEbula1999@localhost:3306/taskpro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

db.init_app(app)
bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()



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
